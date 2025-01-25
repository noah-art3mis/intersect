import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from read_pdf import get_text_from_pdf
from semantic_search import semantic_search_openai
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

    df = pd.read_feather(get_db_filepath(db_name))
    df = df.dropna()
    df = df.drop_duplicates(subset=["description"])

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

    st.metric("Jobs found", len(df))

    st.write("### Most relevant")
    st.write("Original results")
    with st.spinner():
        df_copy = df.copy(deep=True)
        st.dataframe(df_copy[["title", "description"]].head(5))

    st.write("### Best fit")
    # st.write("### Semantic Search")
    st.write("Roles with the highest semantic similarity to your text")
    with st.spinner():
        intersected = semantic_search_openai(df_copy, input_text)  # type: ignore
        semantic_search_view = intersected[
            ["Rank", "Title", "Description", "Link"]
        ].head(5)
        st.dataframe(semantic_search_view, hide_index=True)

    st.write("### Most interesting")
    st.write(
        "Roles that their position changed the most in comparison with the website's original order ('most relevant')"
    )
    with st.spinner():
        sorted = intersected.sort_values("Delta", ascending=False)
        sorted = sorted[["Rank", "Title", "Description"]].head(5)
        st.dataframe(sorted, hide_index=True)

    st.write("### Relevant words")
    st.write("Topic modelling (TF-IDF)")
    with st.spinner():
        wc = tfidf_words(intersected["Description"].tolist())
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
        df_with_pca = pca_df(intersected, "Vector", n_components=2)
        clustered = [
            add_clusters(df_with_pca, i, n_components=2) for i in cluster_range
        ]
        chart = get_chart(clustered[n_clusters])
        st.altair_chart(chart, use_container_width=True)

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
    #     sentences = intersected["Description"].tolist()
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
