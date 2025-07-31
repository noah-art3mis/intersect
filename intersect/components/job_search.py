import streamlit as st
import pandas as pd
import os
from data_sources.reed_client import ReedAPI, reed_jobs_to_dicts
from duckdb_storage import save_jobs_to_duckdb, get_job_statistics
from config.constants import DB_NAME, TABLE_NAME, DATA_SOURCE

def search_and_process_jobs(form_data):
    """Search for jobs and process the results"""
    
    api = ReedAPI()
    
    with st.spinner("🔍 Searching for jobs..."):
        # Build search parameters
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
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        # Search for jobs
        job_result, api_params = api.search_jobs(**search_params)
        
        if job_result:
            st.success(f"✅ Found {len(job_result)} jobs!")
            
            with st.expander("Search parameters"):
                st.write(search_params)
            
            # Convert to DataFrame
            job_dicts = reed_jobs_to_dicts(job_result)
            df = pd.DataFrame(job_dicts)
            
            # Save to DuckDB
            with st.spinner("💾 Saving jobs to database..."):
                save_jobs_to_duckdb(job_dicts, DB_NAME, TABLE_NAME, DATA_SOURCE, api_params)
            
            # Show statistics
            stats = get_job_statistics(DB_NAME, TABLE_NAME)
            if stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total jobs", stats.get('total_jobs', 0))
                with col2:
                    st.metric("Jobs with salary", stats.get('jobs_with_salary', 0))
                with col3:
                    st.metric("Unique employers", stats.get('unique_employers', 0))
            
            return df, search_params
        else:
            st.error("No jobs found with the given criteria.")
            return None, None 