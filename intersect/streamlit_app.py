import pandas as pd
import streamlit as st
from datetime import datetime, timezone
from dotenv import load_dotenv
from embedding import get_embedding
from openai import OpenAI

from utils import add_you
from read_pdf import get_text_from_pdf
from semantic_search import format_columns, similarity_search
from cluster_viz import pca_df, get_chart, add_clusters
from lexical_search import lexical_search
from rerank import rerank_cohere
from tfidf import wordcloud_tfidf, tfidf_words
from ner import wordcloud_ner, ner_count
from permutation import permutation_openai

DEFAULT_CV_PATH = "intersect/data/cvs/j.txt"


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
        """This is a work in progress. Soon enough you will be able to search for your own keywords and locations. For now, you can use the following databases."""
    )

    col1, col2 = st.columns(2)

    # keywords = col1.text_input("Keyword", placeholder="ai", disabled=True)

    db_name = col1.selectbox(
        "Database",
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

    st.write("### Most relevant")
    st.write("Original results")
    with st.spinner():
        st.dataframe(
            df[
                ["i_relevance", "title", "company", "days_ago", "description", "url"]
            ].head(5),
            hide_index=True,
        )

    st.write("### Best fit")
    # st.write("### Semantic Search")
    st.write("Roles with the highest semantic similarity to your text")
    with st.spinner():
        input_embedding = get_embedding(OpenAI(), input_text)

        if input_embedding is None:
            st.error("Failed to generate embedding.")

        result = similarity_search(df_copy, input_embedding)  # type: ignore
        df_semantic = format_columns(result)

        view_semantic = df_semantic[["Rank", "Title", "Description", "Link"]].head(5)
        st.dataframe(view_semantic, hide_index=True)

    st.write("### Most interesting")
    st.write(
        "Roles that their position changed the most in comparison with the website's original order ('most relevant')"
    )
    with st.spinner():
        df_semantic_delta = df_semantic.sort_values("Delta", ascending=False)
        view_semantic_delta = df_semantic_delta[["Rank", "Title", "Description"]].head(
            5
        )
        st.dataframe(view_semantic_delta, hide_index=True)

    st.write("### Relevant words")
    st.write("Topic modelling (TF-IDF)")
    with st.spinner():
        wc = tfidf_words(df_semantic["Description"].tolist())
        wcdf = pd.DataFrame(list(wc.items()), columns=["Word", "Frequency"])
        wordcloud_tfidf(wc)

    st.write("### Cluster Visualization (KMeans + PCA)")
    with st.spinner():
        st.write("Hover over items to see more details")

        cluster_range = [3]
        n_clusters = 0
        # cluster_range = range(1, 6)
        # n_clusters = st.select_slider(
        #     "Number of clusters", options=cluster_range, value=3
        # )
        df_w_you = add_you(df_semantic, input_text, input_embedding)
        df_with_pca = pca_df(df_w_you, "Vector", n_components=2)
        clustered = [
            add_clusters(df_with_pca, i, n_components=2) for i in cluster_range
        ]

        chart = get_chart(clustered[n_clusters])
        st.altair_chart(chart, use_container_width=True)
        st.dataframe(clustered[n_clusters])

    # st.write("### All results")
    # st.dataframe(df_copy, hide_index=True)

    st.write("### Other methods")

    st.write("#### Lexical Search (BM25)")
    with st.spinner():
        df_lexical = df.copy(deep=True)
        bm25_results = lexical_search(input_text, df_lexical["description"].tolist())
        st.dataframe(bm25_results.head(5), hide_index=True)

    st.write("#### Rerank with Cross-encoding")
    with st.spinner():
        df_reranker = df.copy(deep=True)
        reranked_results = rerank_cohere(
            input_text, df_reranker["description"].tolist()
        )
        st.dataframe(reranked_results.head(5), hide_index=True)

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

    # does not follow the prompt
    st.write("#### Permutation Generation (LLM)")
    with st.spinner():
        df_permutation = df.copy(deep=True)
        permutation_results = permutation_openai(
            input_text,
            df_reranker["description"].tolist(),
            top_k=10,
        )
        st.dataframe(permutation_results.head(5), hide_index=True)

st.write("---")
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")
