import pandas as pd
import streamlit as st
from data_sources.reed_client import ReedAPI
from data_sources.theirstack_client import TheirstackAPI

def build_search_params(form_data):
    """Build search parameters from form data"""
    search_params = {
        "keywords": form_data['keywords'] if form_data['keywords'] else None,
        "location_name": form_data['location'] if form_data['location'] else None,
        "results_to_take": form_data['results_to_take'],
        "minimum_salary": form_data['minimum_salary'] if form_data['minimum_salary'] > 0 else None,
    }
    
    # Add contract type filter
    if form_data['contract_type'] != "Any":
        if form_data['contract_type'] == "permanent":
            search_params["permanent"] = True
        elif form_data['contract_type'] == "contract":
            search_params["contract"] = True
        elif form_data['contract_type'] == "temp":
            search_params["temp"] = True
    
    # Add full-time filter
    if form_data['full_time']:
        search_params["full_time"] = True
        
    # Remove None values
    return {k: v for k, v in search_params.items() if v is not None}


def search_jobs(search_params: dict, data_source: str) -> pd.DataFrame:
    
    match data_source:
        case "reed":
            api = ReedAPI()
            jobs = api.search_jobs(**search_params)
            return pd.DataFrame(jobs)
        case "theirstack":
            api = TheirstackAPI("data/new/theirstack.feather")
            jobs = api.search_jobs(**search_params)
            return pd.DataFrame(jobs)
        case _:
            raise ValueError(f"Invalid data source: {data_source}")

def get_display_columns(data_source: str) -> dict:
    """Get display column mapping based on data source"""
    match data_source:
        case "reed":
            return {
                'job_title': 'Job Title',
                'employer_name': 'Company', 
                'location_name': 'Location',
                "applications": "Applicants",
                "salary": "Salary",
                "expiration_date": "Expires",
                'description': 'Description',
                'job_url': 'URL',
            }
        case "theirstack":
            return {
                'title': 'Job Title',
                'employer_name': 'Company', 
                'location': 'Location',
                "salary": "Salary",
                "posted": "Posted",
                'description': 'Description',
                'url': 'URL',
            }
        case _:
            raise ValueError(f"Invalid data source: {data_source}")

def display_job_stats(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total jobs", df.shape[0])
    with col2:
        st.metric("Unique employers", int(df['employer_name'].nunique()))