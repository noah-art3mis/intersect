import streamlit as st
from dotenv import load_dotenv

from components.search_form import render_search_form
from components.job_search import search_and_process_jobs
from components.results_display import process_search
from components.footer import render_footer

load_dotenv()

st.title("Intersect")

st.write("""Find the job you actually want using AI.

Tell me about yourself and I will search for jobs based on vibes. No need to use your CV. Paste the lyrics of your favourite song, the words of a poem or a description of your pet. Any text will do. (Using your CV is also fine.)

This is essentially intersecting two searches - one using a keyword and another using the meaning of a text. You can think of this as searching both for what you want and what you need.
""")

# with st.sidebar:
#     table_size = st.select_slider("Table size", range(3, 11), 5)

form_data = render_search_form()

if form_data['submit']:
    st.write("## Results")
    
    df, search_params = search_and_process_jobs(form_data)
    
    if df is None or len(df) == 0:
        st.error("No jobs found to display")
    else:
        st.write("The tables are interactive. Double click the description to read it.")
        process_search(df, form_data['input_text'])

# Render footer
render_footer()
