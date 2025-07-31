import pandas as pd
import streamlit as st
from datetime import datetime, timezone
from dotenv import load_dotenv
from embedding import get_embedding
from openai import OpenAI
import os
import random

from utils import add_you, add_index
from read_pdf import get_text_from_pdf
from semantic_search import similarity_search
from cluster_viz import pca_df, get_chart, add_clusters
from lexical_search import lexical_search
from rerank import rerank_cohere
from tfidf import wordcloud_tfidf, tfidf_words
from ner import wordcloud_ner, ner_count
from permutation import permutation_openai
from get_jobs import ReedAPI, reed_jobs_to_dicts
from duckdb_storage import save_jobs_to_duckdb, load_jobs_from_duckdb, get_job_statistics

DEFAULT_CV_TEXTS = "Look at you hacker, a pathetic creature of meat and bone, panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?"

DB_NAME = "streamlit_jobs.duckdb"
TABLE_NAME = "latest_search"
DATA_SOURCE = "reed"

load_dotenv()

st.title("Intersect")

"""Find the job you actually want using AI.

Tell me about yourself and I will search for jobs based on vibes. No need to use your CV. Paste the lyrics of your favourite song, the words of a poem or a description of your pet. Any text will do. (Using your CV is also fine.)

This is essentially intersecting two searches - one using a keyword and another using the meaning of a text. You can think of this as searching both for what you want and what you need.
"""

# with st.sidebar:
#     table_size = st.select_slider("Table size", range(3, 11), 5)


with st.form("my_form", border=False):

    st.write("")
    st.write("## About the job")
    st.write(
        """Search for jobs using the Reed.co.uk [Jobseeker API](https://www.reed.co.uk/developers/Jobseeker)."""
    )
    # Job search form
    keywords = st.text_input("Job keywords", placeholder="python developer", help="Enter job title, skills, or keywords")

    with st.expander("Advanced search options"):
        
        st.write("Feel free to leave these blank.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            results_to_take = st.number_input("Number of results", min_value=1, max_value=100, step=10, value=1, help="How many jobs to search for")
            
            minimum_salary = st.number_input("Minimum salary (£)", min_value=0, value=0, step=10000, help="Minimum annual salary")
        
        with col2:
            location = st.text_input("City (UK)", placeholder="london", help="Enter city name")
            
            contract_type = st.selectbox("Contract type", ["Any", "permanent", "contract", "temp"], help="Type of employment")
            
            full_time = st.checkbox("Full time only", value=True, help="Show only full-time positions")

    st.write("")
    st.write("## About you")

    uploaded_file = st.file_uploader("Upload a pdf, or", type="pdf")

    if uploaded_file is not None:
        input_text = get_text_from_pdf(uploaded_file)

        if input_text == "":
            st.error(
                "No text found in pdf. You might have a scanned document, which is not supported."
            )
    else:
        input_text = st.text_area("Paste any text", placeholder=DEFAULT_CV_TEXTS, height=34 * 4)

        if input_text is None:
            input_text = DEFAULT_CV_TEXTS

    st.write("")
    st.write("## Search")

    submit = st.form_submit_button("Search!")


if submit:
    st.write("## Results")
    
    api_key = os.getenv("REED_API_KEY")
    api = ReedAPI()
            
    with st.spinner("🔍 Searching for jobs..."):

        search_params = {
            "keywords": keywords if keywords else None,
            "location_name": location if location else None,
            "results_to_take": results_to_take,
            "minimum_salary": minimum_salary if minimum_salary > 0 else None,
        }
                
        # Add contract type filter
        if contract_type != "Any":
            if contract_type == "permanent":
                search_params["permanent"] = True
            elif contract_type == "contract":
                search_params["contract"] = True
            elif contract_type == "temp":
                search_params["temp"] = True
        
        # Add full-time filter
        if full_time:
            search_params["full_time"] = True
                
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
                
        # Search for jobs
        job_result, api_params = api.search_jobs(**search_params)
        
        if job_result:
            st.success(f"✅ Found {len(job_result)} jobs!")
            
            with st.expander("Search parameters"):
                st.write(search_params)
            
            # Convert to DataFrame for display
            job_dicts = reed_jobs_to_dicts(job_result)
            df = pd.DataFrame(job_dicts)
            original_df = df.copy()
            
            # Save to DuckDB
            with st.spinner("💾 Saving jobs to database..."):
                save_jobs_to_duckdb(job_dicts, DB_NAME, TABLE_NAME, DATA_SOURCE, api_params)
            
            # Show statistics
            stats = get_job_statistics(DB_NAME, TABLE_NAME)
            if stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total jobs", stats.get('total_jobs', 0))
                with col2:
                    st.metric("Jobs with salary", stats.get('jobs_with_salary', 0))
                with col3:
                    st.metric("Unique employers", stats.get('unique_employers', 0))
            
            # Display jobs in a table
            st.write("### Job Listings")
            
            # Select and rename columns for display
            display_columns = {
                'job_title': 'Job Title',
                'employer_name': 'Company', 
                'location_name': 'Location',
                'contract_type': 'Contract Type',
                'job_url': 'Apply',
                'description': 'Description'
            }
            
            # Format salary information
            def format_salary(row):
                min_salary = row['minimum_salary']
                max_salary = row['maximum_salary']
                
                if pd.notna(min_salary) and pd.notna(max_salary):
                    return f"£{min_salary:,} - £{max_salary:,}"
                elif pd.notna(min_salary):
                    return f"From £{min_salary:,}"
                elif pd.notna(max_salary):
                    return f"Up to £{max_salary:,}"
                return "Not specified"

            df['salary'] = df.apply(format_salary, axis=1)
            df = df.drop(columns=['minimum_salary', 'maximum_salary'])
            
    # Continue with existing functionality if we have data
    if df is not None and len(df) > 0:
        st.write("The tables are interactive. Double click the description to read it.")

        ### WORD CLOUD ###
        with st.spinner("Generating word cloud..."):
            wordcloud_tfidf(tfidf_words(df["description"].tolist()))

        ### RELEVANCE ###
        st.write("### Most relevant")
        with st.spinner():
            display_df = df.copy()
            st.dataframe(display_df.rename(columns=display_columns), hide_index=True)

        ### SEMANTIC ###
        st.write("### Best fit")
        with st.spinner():
            input_embedding = get_embedding(OpenAI(), input_text)

            df['embedding'] = df['Description'].apply(get_embedding)

            if input_embedding is None:
                st.error("Failed to generate embedding.")

            df = similarity_search(df, input_embedding)  # type: ignore
            df = add_index(df, "score_semantic", "i_semantic")

        view_semantic = df[
            [
                "id",
                # "i_semantic",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]

        st.dataframe(view_semantic.head(table_size), hide_index=True)

    ### SEMANTIC DELTA ###

    st.write("### Most interesting")
    # st.write("Roles with highest displacement")
    with st.spinner():
        df["delta_semantic"] = df["i_relevance"] - df["i_semantic"]
        df_semantic_delta = df.sort_values("delta_semantic", ascending=False)
        view_semantic_delta = df_semantic_delta[
            [
                "id",
                # "i_semantic",
                # "delta_semantic",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_semantic_delta.head(table_size), hide_index=True)

    ### EMBEDDING PCA ###

    st.write("### Cluster Visualization (KMeans + PCA)")
    with st.spinner():

        st.write("Select tabs for different clustering")
        st.write("Hover over items to see more details")

        df_without_you = df.copy()
        df_you = add_you(df_without_you, input_text, input_embedding)  # type: ignore
        df_pca = pca_df(df_you, "embedding", n_components=2)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["No clusters", "2 clusters", "3 clusters", "4 clusters", "5 clusters"]
        )

        def generate_chart(_df: pd.DataFrame, n_clusters: int) -> None:
            _df = add_clusters(df_pca, n_clusters, n_components=2)
            _df.loc[_df["title"] == "Your text", "Cluster"] = " You"
            chart = get_chart(_df)
            st.altair_chart(chart, use_container_width=True)

        with tab1:
            generate_chart(df_pca, 1)

        with tab2:
            generate_chart(df_pca, 2)

        with tab3:
            generate_chart(df_pca, 3)

        with tab4:
            generate_chart(df_pca, 4)

        with tab5:
            generate_chart(df_pca, 5)

    # st.write("### All results")
    # st.dataframe(df, hide_index=True)

    # st.write("### Other methods")

    ### LEXICAL ###

    st.write("### Lexical Search (BM25)")
    with st.spinner():
        df = lexical_search(input_text, df)
        view_lexical = df.sort_values(by="score_lexical", ascending=False)
        view_lexical = view_lexical[
            [
                "id",
                # "i_lexical",
                # "score_lexical",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_lexical.head(table_size), hide_index=True)

    # st.write("#### Lexical Search Displacement")
    # with st.spinner():
    #     df["delta_lexical"] = df["i_relevance"] - df["i_lexical"]
    #     df_lexical_delta = df.sort_values("delta_lexical", ascending=False)
    #     view_lexical_delta = df_lexical_delta[
    #         [
    #             "id",
    #             # "i_lexical",
    #             # "delta_lexical",
    #             "title",
    #             "company",
    #             "days_ago",
    #             "description",
    #             "url",
    #         ]
    #     ]
    #     st.dataframe(view_lexical_delta.head(table_size), hide_index=True)

    ### RERANKER ###

    st.write("### Rerank with Cross-encoding")
    with st.spinner():
        df = rerank_cohere(input_text, df)
        df = add_index(df, "score_reranker", new_index="i_reranker")
        view_reranked = df.sort_values(by="score_reranker", ascending=False)
        view_reranked = view_reranked[
            [
                "id",
                # "i_reranker",
                # "score_reranker",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_reranked.head(table_size), hide_index=True)

    # st.write("#### Cross-encoding Displacement")
    # with st.spinner():
    #     df["delta_reranker"] = df["i_relevance"] - df["i_reranker"]
    #     df_reranker = df.sort_values("delta_reranker", ascending=False)
    #     view_reranker = df_reranker[
    #         [
    #             "id",
    #             # "i_reranker",
    #             # "delta_reranker",
    #             "title",
    #             "company",
    #             "days_ago",
    #             "description",
    #             "url",
    #         ]
    #     ]
    #     st.dataframe(view_reranker.head(table_size), hide_index=True)

    # st.write("### TF-IDF Table")
    # wc_sorted = wcdf.sort_values(by="Frequency", ascending=False)
    # st.dataframe(wc_sorted, hide_index=True)

    # too slow
    # st.write("### Named entity recognition")
    # with st.spinner():
    #     sentences = df_semantic["Description"].tolist()
    #     entities = ner_count(sentences)
    #     entities_df = pd.DataFrame.from_dict(entities, orient="index")
    #     entities_sorted = entities_df.sort_values(by="0", ascending=False)
    #     st.dataframe(entities_df)
    #     wordcloud_ner(ner_count(sentences))

    ## PERMUTATION ###
    # st.write("#### Permutation Generation (LLM)")
    # with st.spinner():
    #     permutation_results = permutation_openai(
    #         input_text,
    #         df,
    #         top_k=10,
    #     )
    #     st.dataframe(permutation_results)
    #     df = df.merge(permutation_results, how="left", on="i_relevance")
    #     st.dataframe(df, hide_index=True)
    #     view_permutation = df[
    #         [
    #             "i_relevance",
    #             "i_permutation",
    #             "title",
    #             "company",
    #             "days_ago",
    #             "description",
    #             "url",
    #         ]
    #     ].sort_values(by="i_permutation", ascending=False)
    #     st.dataframe(view_permutation.head(table_size), hide_index=True)

st.write("---")
st.write(
    "Made by Gustavo Costa ([Github](https://github.com/noah-art3mis) / [LinkedIn](https://www.linkedin.com/in/gustavoarcos/) / [Website](https://simulacro.co.uk/)) "
)
