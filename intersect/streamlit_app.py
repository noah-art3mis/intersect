import streamlit as st
from dotenv import load_dotenv

from components.search_form import render_search_form
from components.job_search import build_search_params, search_jobs, display_job_stats
from components.results_display import process_search
from components.footer import render_footer
from data_sources.preprocessing import preprocess_jobs

load_dotenv()

st.title("Intersect")

st.write("""Find the job you actually want using AI.

Tell me about yourself and I will search for jobs based on vibes. No need to use your CV. Paste the lyrics of your favourite song, the words of a poem or a description of your pet. Any text will do. (Using your CV is also fine.)

This is essentially intersecting two searches - one using a keyword and another using the meaning of a text. You can think of this as searching both for what you want and what you need.
""")

form_data = render_search_form()

if form_data['submit']:
    st.write("## Results")
        
    with st.spinner("🔍 Searching for jobs..."):
        search_params = build_search_params(form_data)
        df = search_jobs(search_params, "reed")
        df = preprocess_jobs(df)
        
    if df.empty:
        st.error("No jobs found with the given criteria.")
    else:
        st.write("The tables are interactive. Double click the description to read it.")

        display_job_stats(df)
        process_search(df, form_data['input_text'])

render_footer()
