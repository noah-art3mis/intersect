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

DB_FILEPATH = "intersect/data/jobs-144.feather"

load_dotenv()
df = pd.read_feather(DB_FILEPATH)

st.title("Intersect")

"""Find the job you actually want - using AI.

Tell me about yourself and I will search for jobs based on vibes. No need to use your CV. Paste the lyrics of your favourite song, the words of a poem or a description of your pet. Any text will do. (Using your CV is also fine.)
"""

with st.form("my_form", border=False):

    st.write("## About the job")

    col1, col2 = st.columns(2)

    keywords = col1.text_input("Keyword", placeholder="ai", disabled=True)

    keywords = col2.text_input("City (UK)", placeholder="london", disabled=True)

    st.write(
        """This is a work in progress. Soon enough you will be able to search for your own. Sorry!"""
    )

    st.write("## About you")

    uploaded_file = st.file_uploader("Upload a pdf, or", type="pdf")

    if uploaded_file is not None:
        input_text = get_text_from_pdf(uploaded_file)

        if input_text == "":
            st.error(
                "No text found in pdf. You might have a scanned document, which is not supported."
            )
    else:
        with open("intersect/data/raw/cvs/cv2.txt", "r") as f:
            TEXT = f.read()
        input_text = st.text_area("Paste any text", TEXT, height=34 * 4)

    st.write("## Search")

    submit = st.form_submit_button("Search!")


if submit:
    st.write("## Results")
    with st.spinner():
        df_intersect = df.copy(deep=True)
        intersected = semantic_search_openai(df_intersect, input_text)  # type: ignore

    st.metric("Jobs found", len(intersected))

    st.write("### Best fit")
    st.write("Roles with the highest semantic similarity to your text")
    with st.spinner():
        ranked = intersected[["Rank", "Title", "Description", "Link"]].head(5)
        st.dataframe(ranked, hide_index=True)

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
        n_components = 2  # not using 2 will break
        n_clusters = 5
        df_with_pca = pca_df(intersected, "Vector", n_components)
        clustered = add_clusters(df_with_pca, n_clusters, n_components)
        chart = get_chart(clustered)
        st.altair_chart(chart, use_container_width=True)

    # st.write("### All results")
    # st.dataframe(intersected, hide_index=True)

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

    st.write("### TF-IDF Table")
    wc_sorted = wcdf.sort_values(by="Frequency", ascending=False)
    st.dataframe(wc_sorted, hide_index=True)

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
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")