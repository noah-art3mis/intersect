import streamlit as st
import intersect
from sklearn.decomposition import PCA
import pandas as pd
from io import StringIO
from read_pdf import get_text_from_pdf

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

    # reorder and drop columns
    intersected = intersected[
        # ["title", "position_change", "similarity", "description", "embedding"]
        ["title", "position_change", "description"]
    ]

    # rename columns
    intersected.columns = ["Title", "Delta", "Description"]
    # intersected.columns = ["Title", "Delta", "Similarity", "Description", "Vector"]

    st.subheader("Best roles")
    st.write("Roles with the highest semantic similarity to your text")
    st.dataframe(intersected.head(5))

    st.subheader("Highest delta")
    st.write(
        "Roles that their position changed the most in comparison with the website's original order"
    )
    st.dataframe(intersected.sort_values("Delta", ascending=False).head(5))

    st.subheader("All results")
    st.dataframe(intersected)

    # bm25
    # tf idf thing

    # TODO this is wrong clearly
    st.subheader("Cluster Visualization")
    n_components = 2
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(intersected["Vector"].tolist())
    pca_df = pd.DataFrame(
        principal_components, columns=[f"PC{i+1}" for i in range(n_components)]
    )
    st.scatter_chart(pca_df)


st.write("---")
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")
