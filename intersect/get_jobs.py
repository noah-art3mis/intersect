import requests
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import os
import dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ReedJob:
    """Data class to represent a job listing"""
    job_id: int
    employer_id: int
    employer_name: str
    employer_profile_id: Optional[int]
    job_title: str
    description: str
    location_name: str
    minimum_salary: Optional[int]
    maximum_salary: Optional[int]
    yearly_minimum_salary: Optional[int]
    yearly_maximum_salary: Optional[int]
    currency: Optional[str]
    salary_type: Optional[str]
    contract_type: Optional[str]
    job_type: Optional[str]
    expiration_date: Optional[str]
    external_url: Optional[str]
    reed_url: Optional[str]


class ReedAPI:
    """Client for the Reed.co.uk Jobseeker API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Reed API client
        
        Args:
            api_key: Reed.co.uk API key. If None, will try to get from REED_API_KEY env var
        """
        self.api_key = api_key or os.getenv('REED_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set REED_API_KEY environment variable or pass api_key parameter")
        
        self.base_url = "https://www.reed.co.uk/api/1.0"
        self.session = requests.Session()
        self.session.auth = (self.api_key, '')  # Basic auth with API key as username
    
    def search_jobs(self, 
                   keywords: Optional[str] = None,
                   location_name: Optional[str] = None,
                   employer_id: Optional[int] = None,
                   employer_profile_id: Optional[int] = None,
                   distance_from_location: Optional[int] = None,
                   permanent: Optional[bool] = None,
                   contract: Optional[bool] = None,
                   temp: Optional[bool] = None,
                   part_time: Optional[bool] = None,
                   full_time: Optional[bool] = None,
                   minimum_salary: Optional[int] = None,
                   maximum_salary: Optional[int] = None,
                   posted_by_recruitment_agency: Optional[bool] = None,
                   posted_by_direct_employer: Optional[bool] = None,
                   graduate: Optional[bool] = None,
                   results_to_take: Optional[int] = None,
                   results_to_skip: Optional[int] = None) -> list[ReedJob]:
        """
        Search for jobs using the Reed.co.uk API
        
        Args:
            keywords: Search keywords
            location_name: Location of the job
            employer_id: ID of employer posting job
            employer_profile_id: Profile ID of employer posting job
            distance_from_location: Distance from location in miles (default 10)
            permanent: True/false for permanent jobs
            contract: True/false for contract jobs
            temp: True/false for temporary jobs
            part_time: True/false for part-time jobs
            full_time: True/false for full-time jobs
            minimum_salary: Lowest possible salary
            maximum_salary: Highest possible salary
            posted_by_recruitment_agency: True/false for agency-posted jobs
            posted_by_direct_employer: True/false for direct employer jobs
            graduate: True/false for graduate jobs
            results_to_take: Maximum number of results (max 100)
            results_to_skip: Number of results to skip for paging
            
        Returns:
            List of Job objects
        """
        # Build query parameters
        params = {}
        
        if keywords:
            params['keywords'] = keywords
        if location_name:
            params['locationName'] = location_name
        if employer_id:
            params['employerId'] = employer_id
        if employer_profile_id:
            params['employerProfileId'] = employer_profile_id
        if distance_from_location:
            params['distanceFromLocation'] = distance_from_location
        if permanent is not None:
            params['permanent'] = str(permanent).lower()
        if contract is not None:
            params['contract'] = str(contract).lower()
        if temp is not None:
            params['temp'] = str(temp).lower()
        if part_time is not None:
            params['partTime'] = str(part_time).lower()
        if full_time is not None:
            params['fullTime'] = str(full_time).lower()
        if minimum_salary:
            params['minimumSalary'] = minimum_salary
        if maximum_salary:
            params['maximumSalary'] = maximum_salary
        if posted_by_recruitment_agency is not None:
            params['postedByRecruitmentAgency'] = str(posted_by_recruitment_agency).lower()
        if posted_by_direct_employer is not None:
            params['postedByDirectEmployer'] = str(posted_by_direct_employer).lower()
        if graduate is not None:
            params['graduate'] = str(graduate).lower()
        if results_to_take:
            params['resultsToTake'] = min(results_to_take, 100)  # API limit
        if results_to_skip:
            params['resultsToSkip'] = results_to_skip
        
        # Make API request
        url = f"{self.base_url}/search"
        logger.info(f"Making request to: {url}")
        logger.debug(f"Parameters: {params}")
        response = self.session.get(url, params=params)
        
        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            logger.error(f"Response text: {response.text}")
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        # Parse response
        try:
            jobs_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.text}")
            raise Exception(f"Invalid JSON response from API: {e}")
        
        
        # Check if jobs_data is a dictionary with 'results' key
        if isinstance(jobs_data, dict) and 'results' in jobs_data:
            jobs_data = jobs_data['results']
        elif not isinstance(jobs_data, list):
            logger.error(f"Unexpected response format: {type(jobs_data)}")
            logger.error(f"Response content: {response.text}")
            raise Exception(f"Expected list of jobs or dict with 'results' key, got {type(jobs_data)}")
        
        jobs = []
        
        for job_data in jobs_data:
            job = ReedJob(
                job_id=job_data.get('jobId'),
                employer_id=job_data.get('employerId'),
                employer_name=job_data.get('employerName', ''),
                employer_profile_id=job_data.get('employerProfileId'),
                job_title=job_data.get('jobTitle', ''),
                description=job_data.get('description', ''),
                location_name=job_data.get('locationName', ''),
                minimum_salary=job_data.get('minimumSalary'),
                maximum_salary=job_data.get('maximumSalary'),
                yearly_minimum_salary=None,  # Not available in search results
                yearly_maximum_salary=None,  # Not available in search results
                currency=None,  # Not available in search results
                salary_type=None,  # Not available in search results
                contract_type=None,  # Not available in search results
                job_type=None,  # Not available in search results
                expiration_date=None,  # Not available in search results
                external_url=None,  # Not available in search results
                reed_url=None  # Not available in search results
            )
            jobs.append(job)
        
        return jobs
    
    def get_job_details(self, job_id: int) -> Optional[ReedJob]:
        """
        Get detailed information about a specific job
        
        Args:
            job_id: The ID of the job to retrieve
            
        Returns:
            ReedJob object with full details, or None if job not found
        """
        url = f"{self.base_url}/jobs/{job_id}"
        logger.info(f"Making job details request to: {url}")
        response = self.session.get(url)
        
        logger.info(f"Job details response status: {response.status_code}")
        
        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            logger.error(f"Job details response text: {response.text}")
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        try:
            job_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.text}")
            raise Exception(f"Invalid JSON response from API: {e}")
        
        # Check if we got an empty job (no data)
        if not job_data or not job_data.get('jobId'):
            return None
        
        job = ReedJob(
            job_id=job_data.get('jobId'),
            employer_id=job_data.get('employerId'),
            employer_name=job_data.get('employerName', ''),
            employer_profile_id=None,  # Not available in details
            job_title=job_data.get('jobTitle', ''),
            description=job_data.get('jobDescription', ''),
            location_name=job_data.get('locationName', ''),
            minimum_salary=job_data.get('minimumSalary'),
            maximum_salary=job_data.get('maximumSalary'),
            yearly_minimum_salary=job_data.get('yearlyMinimumSalary'),
            yearly_maximum_salary=job_data.get('yearlyMaximumSalary'),
            currency=job_data.get('currency'),
            salary_type=job_data.get('salaryType'),
            contract_type=job_data.get('contractType'),
            job_type=job_data.get('jobType'),
            expiration_date=job_data.get('expirationDate'),
            external_url=job_data.get('externalUrl'),
            reed_url=job_data.get('url')
        )
        
        return job


def main():
    """Example usage of the Reed API client"""
    
    dotenv.load_dotenv()
    api_key = os.getenv("REED_API_KEY")
    
    try:
        # Initialize the API client
        api = ReedAPI()
        
        logger.info(f"API Key configured: {'Yes' if api.api_key else 'No'}")
        logger.info("🔍 Searching for Python developer jobs in London...")
        
        # Search for Python developer jobs in London
        job_result = api.search_jobs(
            keywords="Python developer",
            location_name="London",
            results_to_take=5
        )
        logger.info(f"Found {len(job_result)} jobs:")
        print("-" * 50)
        
        for i, job in enumerate(job_result, 1):
            print(f"{i}. {job.job_title}")
            print(f"   Company: {job.employer_name}")
            print(f"   Location: {job.location_name}")
            if job.minimum_salary and job.maximum_salary:
                print(f"   Salary: £{job.minimum_salary:,} - £{job.maximum_salary:,}")
            elif job.minimum_salary:
                print(f"   Salary: From £{job.minimum_salary:,}")
            print(f"   Job ID: {job.job_id}")
            print()
        
        # Get detailed information for the first job
        if job_result:
            logger.info("📋 Getting detailed information for the first job...")
            detailed_job = api.get_job_details(job_result[0].job_id)
            
            if detailed_job:
                print(f"Detailed job information for: {detailed_job.job_title}")
                print(f"Company: {detailed_job.employer_name}")
                print(f"Location: {detailed_job.location_name}")
                print(f"Contract Type: {detailed_job.contract_type}")
                print(f"Job Type: {detailed_job.job_type}")
                if detailed_job.yearly_minimum_salary and detailed_job.yearly_maximum_salary:
                    print(f"Yearly Salary: £{detailed_job.yearly_minimum_salary:,} - £{detailed_job.yearly_maximum_salary:,}")
                if detailed_job.reed_url:
                    print(f"Apply here: {detailed_job.reed_url}")
                print(f"Description: {detailed_job.description[:200]}...")
            else:
                logger.warning("Could not retrieve detailed job information")
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        print("Please set your REED_API_KEY environment variable:")
        print("export REED_API_KEY='your_api_key_here'")


if __name__ == "__main__":
    main()