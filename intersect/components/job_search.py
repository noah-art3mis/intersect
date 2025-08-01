import pandas as pd
import streamlit as st
from data_sources.reed_client import ReedAPI
from data_sources.theirstack_client import TheirstackAPI


def build_search_params(form_data):
    """Build search parameters from form data"""
    search_params = {
        "keywords": form_data["keywords"] if form_data["keywords"] else None,
        "location_name": form_data["location"] if form_data["location"] else None,
        "results_to_take": form_data["results_to_take"],
        "minimum_salary": (
            form_data["minimum_salary"] if form_data["minimum_salary"] > 0 else None
        ),
    }

    # Add contract type filter
    if form_data["contract_type"] != "Any":
        if form_data["contract_type"] == "permanent":
            search_params["permanent"] = True
        elif form_data["contract_type"] == "contract":
            search_params["contract"] = True
        elif form_data["contract_type"] == "temp":
            search_params["temp"] = True

    # Add full-time filter
    if form_data["full_time"]:
        search_params["full_time"] = True

    # Remove None values
    return {k: v for k, v in search_params.items() if v is not None}


def search_jobs(search_params: dict, data_source: str) -> pd.DataFrame:

    def get_api_client(data_source: str):
        match data_source:
            case "reed":
                return ReedAPI()
            case "theirstack":
                return TheirstackAPI("data/new/theirstack.feather")
            case _:
                raise ValueError(f"Invalid data source: {data_source}")

    api = get_api_client(data_source)
    jobs = api.search_jobs(**search_params)
    return pd.DataFrame([job.to_dict() for job in jobs])


def display_job_stats(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total jobs", df.shape[0])
    with col2:
        st.metric("Unique employers", int(df["employer"].nunique()))
