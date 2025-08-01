import streamlit as st
from utils.read_pdf import get_text_from_pdf
from config.constants import DEFAULT_INPUT_TEXT, DEFAULT_KEYWORDS


def render_search_form():
    """Render the job search form and return form data"""

    with st.form("my_form", border=False):
        st.write("")
        st.write("## About the job")
        st.write(
            """Search for jobs using the Reed.co.uk [Jobseeker API](https://www.reed.co.uk/developers/Jobseeker)."""
        )

        # Job search form
        keywords = st.text_input(
            "Job keywords",
            placeholder=DEFAULT_KEYWORDS,
            help="Enter job title, skills, or keywords",
        )
        if keywords == "":
            keywords = DEFAULT_KEYWORDS

        with st.expander("Advanced search options"):
            st.write("Feel free to leave these blank.")

            # Data source selection
            data_source = st.selectbox(
                "Data source",
                ["reed"],
                # ["theirstack", "reed"], # DEBUG
                help="Choose which job database to search",
            )

            col1, col2 = st.columns(2)

            with col1:
                results_to_take = st.number_input(
                    "Number of results",
                    min_value=1,
                    max_value=100,
                    step=10,
                    value=20,
                    help="How many jobs to search for",
                )
                minimum_salary = st.number_input(
                    "Minimum salary (£)",
                    min_value=0,
                    value=0,
                    step=10000,
                    help="Minimum annual salary",
                )

            with col2:
                location = st.text_input(
                    "City (UK)", placeholder="london", help="Enter city name"
                )
                contract_type = st.selectbox(
                    "Contract type",
                    ["Any", "permanent", "contract", "temp"],
                    help="Type of employment",
                )
                full_time = st.checkbox(
                    "Full time only", value=True, help="Show only full-time positions"
                )

        st.write("")
        st.write("## About you")

        uploaded_file = st.file_uploader("Upload a pdf, or", type="pdf")

        if uploaded_file is not None:
            input_text = get_text_from_pdf(uploaded_file)
            if input_text == "":
                st.error(
                    "No text found in pdf. You might have a scanned document, which is not supported."
                )
        else:
            input_text = st.text_area(
                "Paste any text", placeholder=DEFAULT_INPUT_TEXT, height=34 * 4
            )
            if input_text is None or input_text.strip() == "":
                input_text = DEFAULT_INPUT_TEXT

        st.write("")
        st.write("## Search")
        submit = st.form_submit_button("Search!")

        return {
            "submit": submit,
            "keywords": keywords,
            "location": location,
            "results_to_take": results_to_take,
            "minimum_salary": minimum_salary,
            "contract_type": contract_type,
            "full_time": full_time,
            "input_text": input_text,
            "data_source": data_source,
        }
