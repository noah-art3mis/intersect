import streamlit as st
import intersect

DB_FILEPATH = "intersect/data/jobs.feather"

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
    input_text = st.text_area("Paste CV here", TEXT, height=34 * 8)
    submit = st.form_submit_button("Intersect!")

if submit:
    intersected = intersect.intersect(DB_FILEPATH, input_text)  # type: ignore

    st.write("---")
    
    st.subheader("Best role")
    st.dataframe(intersected.head(1))

    st.subheader("Highest change")
    st.dataframe(intersected.sort_values("Change", ascending=False).head(1))

    st.subheader("All results")
    st.dataframe(intersected)


st.write("---")
st.write("Made by [Gustavo Costa](https://github.com/noah-art3mis)")
