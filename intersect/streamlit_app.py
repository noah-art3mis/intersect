import streamlit as st
from intersect import intersect

DB_FILEPATH = "intersect/data/jobs.feather"

with open("intersect/data/raw/cvs/cv1.txt", "r") as f:
    TEXT = f.read()

st.title("Intersect")
st.write("Find the job you actually want by using AI")

st.write(
    "This is a tool to find similar jobs based on your resume. It uses OpenAI embeddings to find similar jobs."
)


with st.form("my_form", border=False):
    st.write("")
    input_text = st.text_area("Paste CV here", TEXT, height=34 * 8)
    submit = st.form_submit_button("Intersect!")

if submit:
    intersected = intersect(DB_FILEPATH, input_text)

    st.subheader("Results")
    st.dataframe(intersected)
