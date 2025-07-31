import pandas as pd
import json
from typing import Optional, Dict, Any
from pathlib import Path


class TheirstackAPI:
    """Client for loading and searching Theirstack job data"""
    
    def __init__(self, data_path: str):
        """Initialize the Theirstack API client"""
        self.data_path = Path(__file__).parent.parent / data_path
        self._load_data()
    
    def _load_data(self):
        """Load the theirstack CSV data"""
        try:
            self.df = pd.read_csv(self.data_path)
            # Convert JSON columns
            self.df['hiring_team'] = self.df['hiring_team'].apply(
                lambda x: json.loads(x) if pd.notna(x) and x != '' else {}
            )
            self.df['company'] = self.df['company'].apply(
                lambda x: json.loads(x) if pd.notna(x) and x != '' else {}
            )
            self.df['country_codes'] = self.df['country_codes'].apply(
                lambda x: json.loads(x) if pd.notna(x) and x != '' else []
            )
        except Exception as e:
            raise Exception(f"Failed to load theirstack data: {e}")
    
    def search_jobs(self, 
                   keywords: Optional[str] = None,
                   location_name: Optional[str] = None,
                   results_to_take: int = 100,
                   minimum_salary: Optional[int] = None,
                   permanent: Optional[bool] = None,
                   contract: Optional[bool] = None,
                   temp: Optional[bool] = None,
                   full_time: Optional[bool] = None) -> list[Dict[str, Any]]:
        """
        Search jobs in the theirstack dataset - loads entire dataset
        
        Args:
            keywords: Keywords to search in job title and description
            location_name: Location to filter by
            results_to_take: Maximum number of results to return
            minimum_salary: Minimum salary filter (in USD)
            permanent: Filter for permanent jobs
            contract: Filter for contract jobs
            temp: Filter for temporary jobs
            full_time: Filter for full-time jobs
            
        Returns:
            List of job dictionaries
        """
        # Load entire dataset without filtering
        filtered_df = self.df.copy()
        
        # Only limit results if specified
        if results_to_take and results_to_take < len(filtered_df):
            filtered_df = filtered_df.head(results_to_take)
        
        # Convert to list of dictionaries with essential columns
        jobs = []
        for _, row in filtered_df.iterrows():
            job = {
                'job_id': str(row['id']),
                'title': row['job_title'],
                'description': row['description'],
                'employer_name': row['company_name'],
                'location': row['location'],
                'salary': row['salary_string'],
                'salary_currency': row['salary_currency'],
                'url': row['url'],
                'posted': row['date_posted']
            }
            jobs.append(job)
        
        return jobs 