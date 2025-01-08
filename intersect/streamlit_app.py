import streamlit as st
import intersect
from sklearn.decomposition import PCA
import pandas as pd
from io import StringIO

DB_FILEPATH = "intersect/data/jobs-144.feather"

with open("intersect/data/raw/cvs/cv2.txt", "r") as f:
    TEXT = f.read()

st.title("Intersect")
st.write("Find the job you actually want - using AI")

st.write(
    "Finds jobs based on vibes instead of specific parameters. This is not supposed to substitute manual search, but to make it easier by ordering the results by relevance."
)

st.write(
    "Uses a similarity search workflow with embedding models to compare your CV with jobs descriptions. Reorders listings based on similarity with the input text, not unlike a [recommendation](https://cookbook.openai.com/examples/recommendation_using_embeddings) algorithm."
)


with st.form("my_form", border=False):
    st.write("")
    st.write("Upload your CV as a pdf or paste it as text below")

    uploaded_file = st.file_uploader("Choose your .pdf file")

    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()

        input_text = st.text_area("Extracted CV", string_data, height=34 * 8)
    else:
        input_text = st.text_area("Or paste it here", TEXT, height=34 * 8)

    submit = st.form_submit_button("Intersect!")


if submit:
    intersected = intersect.intersect(DB_FILEPATH, input_text)  # type: ignore

    # reorder and drop columns
    intersected = intersected[
        ["title", "position_change", "similarity", "description", "embedding"]
    ]
    # rename columns
    intersected.columns = ["Title", "Change", "Similarity", "Description", "Vector"]

    st.write("---")

    st.subheader("Best role")
    st.dataframe(intersected.head(1))

    st.subheader("Highest change")
    st.dataframe(intersected.sort_values("Change", ascending=False).head(1))

    st.subheader("All results")
    st.dataframe(intersected)

    # TODO this is wrong clearly
    st.subheader("Cluster Visualization")
    n_components = 2
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(intersected["Vector"].tolist())
    pca_df = pd.DataFrame(
        principal_components, columns=[f"PC{i+1}" for i in range(n_components)]
    )
    st.scatter_chart(pca_df)

    # do some kind of tf idf thing
    # bm25

st.write("---")
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")
