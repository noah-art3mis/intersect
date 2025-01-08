import streamlit as st

import intersect
from read_pdf import get_text_from_pdf
from cluster_viz import pca_df, get_chart

DB_FILEPATH = "intersect/data/jobs-144.feather"


st.title("Intersect")
st.write("Find the job you actually want - using AI")

st.write(
    "Finds jobs based on vibes instead of specific parameters. This is not supposed to substitute manual search, but to make it easier by ordering the results by relevance."
)

st.write(
    "Uses a similarity search workflow with embedding models to compare your CV with jobs descriptions. Reorders listings based on similarity with the input text, not unlike a [recommendation](https://cookbook.openai.com/examples/recommendation_using_embeddings) algorithm."
)

st.write("## Usage")

with st.form("my_form", border=False):
    st.write("")
    st.write("Upload your CV as a pdf or paste it as text below")

    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    if uploaded_file is not None:
        input_text = get_text_from_pdf(uploaded_file)

        if input_text == "":
            st.error(
                "No text found in pdf. You might have a scanned document, which is not supported."
            )
    else:
        with open("intersect/data/raw/cvs/cv2.txt", "r") as f:
            TEXT = f.read()
        input_text = st.text_area("Or paste it here", TEXT, height=34 * 4)

    submit = st.form_submit_button("Intersect!")


if submit:
    st.write("---")
    st.write("## Results")

    with st.spinner("Loading..."):
        intersected = intersect.intersect(DB_FILEPATH, input_text)  # type: ignore

    st.metric("Jobs found", len(intersected))

    st.subheader("Best fit")
    st.write("Roles with the highest semantic similarity to your text")
    ranked = intersected[["Rank", "Title", "Description"]].head(5)
    st.dataframe(ranked, hide_index=True)

    st.subheader("Most interesting")
    st.write(
        "Roles that their position changed the most in comparison with the website's original order ('most relevant')"
    )
    sorted = intersected.sort_values("Delta", ascending=False)
    sorted = sorted[["Rank", "Title", "Description"]].head(5)
    st.dataframe(sorted, hide_index=True)

    st.subheader("Prominent words in the jobs")
    # TODO named entity recognition

    st.subheader("Words that show up in your CV")
    # TODO topic modelling

    st.subheader("Cluster Visualization")
    df_with_pca = pca_df(intersected, "Vector")
    chart = get_chart(df_with_pca)
    st.altair_chart(chart, use_container_width=True)

    st.subheader("All results")
    st.dataframe(intersected, hide_index=True)

    st.subheader("Comparison with ")
    st.write("### BM25")
    st.write("### MTEB")
    st.write("### reranker")
    st.write("### LLM")

st.write("---")
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")
