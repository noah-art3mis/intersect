import pandas as pd
import streamlit as st
from datetime import datetime, timezone
from dotenv import load_dotenv
from embedding import get_embedding
from openai import OpenAI

from utils import add_you, add_index
from read_pdf import get_text_from_pdf
from semantic_search import similarity_search
from cluster_viz import pca_df, get_chart, add_clusters
from lexical_search import lexical_search
from rerank import rerank_cohere
from tfidf import wordcloud_tfidf, tfidf_words
from ner import wordcloud_ner, ner_count
from permutation import permutation_openai

DEFAULT_CV_PATH = "intersect/data/cvs/g.txt"
TABLE_SIZE = 5


def get_current_dbs() -> list[str]:
    return [
        "ai",
        "change",
        "data",
        "facilitator",
        "fun",
        "law-ai",
        "law",
        "leadership",
    ]


def get_db_filepath(db_name: str) -> str:
    return f"intersect/data/{db_name}.feather"


load_dotenv()

st.title("Intersect")

"""Find the job you actually want - using AI.

Tell me about yourself and I will search for jobs based on vibes. No need to use your CV. Paste the lyrics of your favourite song, the words of a poem or a description of your pet. Any text will do. (Using your CV is also fine.)
"""

with st.form("my_form", border=False):

    st.write("## About the job")

    st.write(
        """This is a work in progress. Soon enough you will be able to search for your own keywords and locations. For now, you can use the following keywords:."""
    )

    col1, col2 = st.columns(2)

    # keywords = col1.text_input("Keyword", placeholder="ai", disabled=True)

    db_name = col1.selectbox(
        "Keyword",
        get_current_dbs(),
        index=0,
    )

    original_df = pd.read_feather(get_db_filepath(db_name))
    original_df = original_df.dropna()
    original_df = original_df.drop_duplicates(subset=["description"])
    original_df["i_relevance"] = original_df.index
    original_df["timestamp"] = pd.to_datetime(original_df["posted"], utc=True)
    now = datetime.now(timezone.utc)
    original_df["days_ago"] = (now - original_df["timestamp"]).dt.days  # type: ignore
    df = original_df.copy(deep=True)

    location = col2.text_input("City (UK)", placeholder="london", disabled=True)

    st.write("## About you")
    uploaded_file = st.file_uploader("Upload a pdf, or", type="pdf")

    if uploaded_file is not None:
        input_text = get_text_from_pdf(uploaded_file)

        if input_text == "":
            st.error(
                "No text found in pdf. You might have a scanned document, which is not supported."
            )
    else:
        with open(DEFAULT_CV_PATH, "r") as f:
            TEXT = f.read()
        input_text = st.text_area("Paste any text", TEXT, height=34 * 4)

    st.write("## Search")

    submit = st.form_submit_button("Search!")


with st.spinner("Looking for jobs..."):
    pass

with st.spinner("Scraping job descriptions..."):
    pass

with st.spinner("Generating embeddings..."):
    pass

if submit:
    st.write("## Results")

    st.metric("Jobs found", len(original_df))

    st.write("The tables are interactive. Click on a row to view the full description.")

    ### RELEVANCE ###

    st.write("### Most relevant")
    st.write("Original results")
    with st.spinner():
        view_relevance = df[
            [
                "i_relevance",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_relevance.head(TABLE_SIZE), hide_index=True)

    ### SEMANTIC ###

    st.write("### Best fit")
    # st.write("### Semantic Search")
    st.write("Roles with the highest semantic similarity")
    with st.spinner():
        input_embedding = get_embedding(OpenAI(), input_text)

        if input_embedding is None:
            st.error("Failed to generate embedding.")

        df = similarity_search(df, input_embedding)  # type: ignore
        df = add_index(df, "score_semantic", "i_semantic")

        view_semantic = df[
            [
                "i_relevance",
                "i_semantic",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]

        st.dataframe(view_semantic.head(TABLE_SIZE), hide_index=True)

    ### SEMANTIC DELTA ###

    st.write("### Most interesting")
    st.write("Roles with highest displacement")
    with st.spinner():
        df["delta_semantic"] = df["i_relevance"] - df["i_semantic"]
        df_semantic_delta = df.sort_values("delta_semantic", ascending=False)
        view_semantic_delta = df_semantic_delta[
            [
                "i_relevance",
                "i_semantic",
                "delta_semantic",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_semantic_delta.head(TABLE_SIZE), hide_index=True)

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

    ### TFDIF ###

    st.write("### Relevant words")
    st.write("Topic modelling (TF-IDF)")
    with st.spinner():
        wc = tfidf_words(df["description"].tolist())
        wcdf = pd.DataFrame(list(wc.items()), columns=["Word", "Frequency"])
        wordcloud_tfidf(wc)

    # st.write("### All results")
    # st.dataframe(df, hide_index=True)

    st.write("### Other methods")

    ### LEXICAL ###

    st.write("#### Lexical Search (BM25)")
    with st.spinner():
        df = lexical_search(input_text, df)
        view_lexical = df.sort_values(by="score_lexical", ascending=False)
        view_lexical = view_lexical[
            [
                "i_relevance",
                "i_lexical",
                "score_lexical",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_lexical.head(TABLE_SIZE), hide_index=True)

    st.write("#### Lexical Search Displacement")
    with st.spinner():
        df["delta_lexical"] = df["i_relevance"] - df["i_lexical"]
        df_lexical_delta = df.sort_values("delta_lexical", ascending=False)
        view_lexical_delta = df_lexical_delta[
            [
                "i_relevance",
                "i_lexical",
                "delta_lexical",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_lexical_delta.head(TABLE_SIZE), hide_index=True)

    ### RERANKER ###

    st.write("#### Rerank with Cross-encoding")
    with st.spinner():
        df = rerank_cohere(input_text, df)
        df = add_index(df, "score_reranker", new_index="i_reranker")
        view_reranked = df.sort_values(by="score_reranker", ascending=False)
        view_reranked = view_reranked[
            [
                "i_relevance",
                "i_reranker",
                "score_reranker",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_reranked.head(TABLE_SIZE), hide_index=True)

    st.write("#### Cross-encoding Displacement")
    with st.spinner():
        df["delta_reranker"] = df["i_relevance"] - df["i_reranker"]
        df_reranker = df.sort_values("delta_reranker", ascending=False)
        view_reranker = df_reranker[
            [
                "i_relevance",
                "i_reranker",
                "delta_reranker",
                "title",
                "company",
                "days_ago",
                "description",
                "url",
            ]
        ]
        st.dataframe(view_reranker.head(TABLE_SIZE), hide_index=True)

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

    ### PERMUTATION ###

    # does not follow the prompt
    # st.write("#### Permutation Generation (LLM)")
    # with st.spinner():
    #     df_permutation = df.copy(deep=True)
    #     permutation_results = permutation_openai(
    #         input_text,
    #         df_reranker["description"].tolist(),
    #         top_k=10,
    #     )
    #     st.dataframe(permutation_results.head(5), hide_index=True)

st.write("---")
st.write(
    "Made by Gustavo Costa ([Github](https://github.com/noah-art3mis) / [LinkedIn](https://www.linkedin.com/in/gustavoarcos/) / [Website](https://simulacro.co.uk/)) "
)
