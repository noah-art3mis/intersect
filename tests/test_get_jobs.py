import pytest
import os
from intersect.get_jobs import ReedAPI, ReedJob, reed_jobs_to_dicts


class TestReedJob:
    """Test the ReedJob dataclass"""
    
    def test_reed_job_creation(self):
        """Test creating a ReedJob instance"""
        job = ReedJob(
            job_id=12345,
            employer_id=67890,
            employer_name="Test Company",
            employer_profile_id=11111,
            job_title="Software Engineer",
            description="A great job opportunity",
            location_name="London",
            minimum_salary=50000,
            maximum_salary=70000,
            yearly_minimum_salary=50000,
            yearly_maximum_salary=70000,
            currency="GBP",
            salary_type="yearly",
            contract_type="permanent",
            job_type="full-time",
            expiration_date="2024-12-31",
            external_url="https://example.com/job",
            reed_url="https://reed.co.uk/job/12345"
        )
        
        assert job.job_id == 12345
        assert job.employer_name == "Test Company"
        assert job.job_title == "Software Engineer"


class TestReedJobsToDicts:
    """Test the reed_jobs_to_dicts function"""
    
    def test_reed_jobs_to_dicts(self):
        """Test converting ReedJob objects to dictionaries"""
        # Create sample ReedJob objects
        job1 = ReedJob(
            job_id=1,
            employer_id=101,
            employer_name="Test Company 1",
            employer_profile_id=1001,
            job_title="Python Developer",
            description="We are looking for a Python developer",
            location_name="London",
            minimum_salary=50000,
            maximum_salary=70000,
            yearly_minimum_salary=50000,
            yearly_maximum_salary=70000,
            currency="GBP",
            salary_type="yearly",
            contract_type="permanent",
            job_type="full-time",
            expiration_date="2024-12-31",
            external_url="https://example.com/job1",
            reed_url="https://reed.co.uk/job1"
        )
        
        job2 = ReedJob(
            job_id=2,
            employer_id=102,
            employer_name="Test Company 2",
            employer_profile_id=None,
            job_title="Data Scientist",
            description="We are looking for a data scientist",
            location_name="Manchester",
            minimum_salary=None,
            maximum_salary=None,
            yearly_minimum_salary=None,
            yearly_maximum_salary=None,
            currency=None,
            salary_type=None,
            contract_type="contract",
            job_type="full-time",
            expiration_date=None,
            external_url=None,
            reed_url="https://reed.co.uk/job2"
        )
        
        jobs = [job1, job2]
        
        # Convert to dictionaries
        job_dicts = reed_jobs_to_dicts(jobs)
        
        # Verify conversion
        assert len(job_dicts) == 2
        assert isinstance(job_dicts, list)
        
        # Check first job
        job1_dict = job_dicts[0]
        assert job1_dict['job_id'] == 1
        assert job1_dict['employer_name'] == "Test Company 1"
        assert job1_dict['job_title'] == "Python Developer"
        assert job1_dict['minimum_salary'] == 50000
        assert job1_dict['maximum_salary'] == 70000
        assert job1_dict['employer_profile_id'] == 1001
        assert job1_dict['currency'] == "GBP"
        
        # Check second job (with null values)
        job2_dict = job_dicts[1]
        assert job2_dict['job_id'] == 2
        assert job2_dict['employer_name'] == "Test Company 2"
        assert job2_dict['employer_profile_id'] is None
        assert job2_dict['minimum_salary'] is None
        assert job2_dict['maximum_salary'] is None
        assert job2_dict['currency'] is None
        assert job2_dict['external_url'] is None
    
    def test_reed_jobs_to_dicts_empty_list(self):
        """Test converting empty list of ReedJob objects"""
        job_dicts = reed_jobs_to_dicts([])
        assert job_dicts == []
        assert isinstance(job_dicts, list)


class TestReedAPIIntegration:
    """Integration tests for the ReedAPI class"""
    
    @pytest.fixture
    def api_client(self):
        """Create an API client for testing"""
        api_key = os.getenv('REED_API_KEY')
        if not api_key:
            pytest.skip("REED_API_KEY environment variable not set")
        return ReedAPI(api_key=api_key)
    
    def test_api_initialization(self, api_client):
        """Test that the API client initializes correctly"""
        assert api_client.api_key is not None
        assert api_client.base_url == "https://www.reed.co.uk/api/1.0"
    
    def test_search_jobs(self, api_client):
        """Test basic job search functionality"""
        jobs, api_params = api_client.search_jobs(
            keywords="Python",
            location_name="London",
            results_to_take=3
        )
        
        assert isinstance(jobs, list)
        assert len(jobs) <= 3
        assert isinstance(api_params, dict)
        assert 'keywords' in api_params
        assert 'location_name' in api_params
        
        if jobs:
            job = jobs[0]
            assert job.job_id is not None
            assert job.employer_name is not None
            assert job.job_title is not None
    
    def test_get_job_details(self, api_client):
        """Test getting detailed job information"""
        # First search for a job to get a valid job ID
        jobs, api_params = api_client.search_jobs(
            keywords="Python",
            location_name="London",
            results_to_take=1
        )
        
        if jobs:
            job_id = jobs[0].job_id
            detailed_job = api_client.get_job_details(job_id)
            
            assert detailed_job is not None
            assert detailed_job.job_id == job_id
            assert detailed_job.job_title is not None
            assert detailed_job.description is not None
    
    def test_search_with_filters(self, api_client):
        """Test job search with filters"""
        jobs, api_params = api_client.search_jobs(
            keywords="developer",
            location_name="Manchester",
            permanent=True,
            minimum_salary=30000,
            results_to_take=2
        )
        
        assert isinstance(jobs, list)
        assert isinstance(api_params, dict)
        if jobs:
            for job in jobs:
                assert job.job_id is not None
                assert job.employer_name is not None


if __name__ == "__main__":
    pytest.main([__file__]) 