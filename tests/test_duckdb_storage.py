"""
Tests for the DuckDB storage module
"""

import pytest
import tempfile
import os
import json
from datetime import datetime
from typing import Dict, List, Any

from intersect.duckdb_storage import (
    save_jobs_to_duckdb,
    load_jobs_from_duckdb,
    query_jobs_from_duckdb,
    get_job_statistics
)


class TestDuckDBStorage:
    """Test cases for DuckDB storage functionality"""
    
    @pytest.fixture
    def sample_jobs(self):
        """Sample job data for testing"""
        return [
            {
                'job_id': 1,
                'employer_id': 101,
                'employer_name': 'Test Company 1',
                'employer_profile_id': 1001,
                'job_title': 'Python Developer',
                'description': 'We are looking for a Python developer',
                'location_name': 'London',
                'minimum_salary': 50000,
                'maximum_salary': 70000,
                'yearly_minimum_salary': 50000,
                'yearly_maximum_salary': 70000,
                'currency': 'GBP',
                'salary_type': 'yearly',
                'contract_type': 'permanent',
                'job_type': 'full-time',
                'expiration_date': '2024-12-31',
                'external_url': 'https://example.com/job1',
                'reed_url': 'https://reed.co.uk/job1'
            },
            {
                'job_id': 2,
                'employer_id': 102,
                'employer_name': 'Test Company 2',
                'employer_profile_id': None,
                'job_title': 'Data Scientist',
                'description': 'We are looking for a data scientist',
                'location_name': 'Manchester',
                'minimum_salary': 60000,
                'maximum_salary': 80000,
                'yearly_minimum_salary': None,
                'yearly_maximum_salary': None,
                'currency': 'GBP',
                'salary_type': 'yearly',
                'contract_type': 'contract',
                'job_type': 'full-time',
                'expiration_date': None,
                'external_url': None,
                'reed_url': 'https://reed.co.uk/job2'
            },
            {
                'job_id': 3,
                'employer_id': 101,
                'employer_name': 'Test Company 1',
                'employer_profile_id': 1001,
                'job_title': 'Senior Python Developer',
                'description': 'We are looking for a senior Python developer',
                'location_name': 'London',
                'minimum_salary': None,
                'maximum_salary': None,
                'yearly_minimum_salary': None,
                'yearly_maximum_salary': None,
                'currency': None,
                'salary_type': None,
                'contract_type': 'permanent',
                'job_type': 'full-time',
                'expiration_date': '2024-12-31',
                'external_url': 'https://example.com/job3',
                'reed_url': 'https://reed.co.uk/job3'
            }
        ]
    
    @pytest.fixture
    def sample_api_params(self):
        """Sample API parameters for testing"""
        return {
            'keywords': 'python developer',
            'location_name': 'London',
            'results_to_take': 10,
            'minimum_salary': 40000
        }
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path"""
        # Create a temporary file path without creating the file
        db_path = tempfile.mktemp(suffix='.duckdb')
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_save_jobs_to_duckdb(self, sample_jobs, sample_api_params, temp_db_path):
        """Test saving jobs to DuckDB"""
        # Save jobs
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", sample_api_params)
        
        # Verify the database file was created in the data directory
        data_dir = os.path.join(os.path.dirname(__file__), "..", "intersect", "data", "duckdb")
        full_db_path = os.path.join(data_dir, temp_db_path)
        assert os.path.exists(full_db_path)
        
        # Load jobs back and verify
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        # Check that all jobs were saved
        assert len(loaded_jobs) == len(sample_jobs)
        
        # Check that metadata was added
        for job in loaded_jobs:
            assert job['data_source'] == 'reed'
            assert job['api_parameters'] == json.dumps(sample_api_params)
            assert 'created_at' in job
            assert job['created_at'] is not None
    
    def test_save_jobs_to_duckdb_no_api_params(self, sample_jobs, temp_db_path):
        """Test saving jobs without API parameters"""
        # Save jobs without API parameters
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", None)
        
        # Load jobs back and verify
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        # Check that all jobs were saved
        assert len(loaded_jobs) == len(sample_jobs)
        
        # Check that metadata was added correctly
        for job in loaded_jobs:
            assert job['data_source'] == 'reed'
            assert job['api_parameters'] is None
            assert 'created_at' in job
    
    def test_save_jobs_to_duckdb_empty_list(self, temp_db_path):
        """Test saving empty job list"""
        # Should not raise an exception
        save_jobs_to_duckdb([], temp_db_path, "test_jobs", "reed", None)
        
        # Database should be created even with empty list
        data_dir = os.path.join(os.path.dirname(__file__), "..", "intersect", "data", "duckdb")
        full_db_path = os.path.join(data_dir, temp_db_path)
        assert os.path.exists(full_db_path)
    
    def test_load_jobs_from_duckdb(self, sample_jobs, sample_api_params, temp_db_path):
        """Test loading jobs from DuckDB"""
        # Save jobs first
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", sample_api_params)
        
        # Load jobs
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        # Verify all jobs were loaded
        assert len(loaded_jobs) == len(sample_jobs)
        
        # Verify job data integrity
        for original, loaded in zip(sample_jobs, loaded_jobs):
            for key in original:
                if original[key] is not None:
                    assert loaded[key] == original[key]
    
    def test_load_jobs_from_duckdb_nonexistent_table(self, temp_db_path):
        """Test loading from non-existent table"""
        # Should return empty list, not raise exception
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "nonexistent_table")
        assert loaded_jobs == []
    
    def test_load_jobs_from_duckdb_nonexistent_db(self):
        """Test loading from non-existent database"""
        # Should return empty list, not raise exception
        loaded_jobs = load_jobs_from_duckdb("nonexistent.duckdb", "test_jobs")
        assert loaded_jobs == []
    
    def test_query_jobs_from_duckdb(self, sample_jobs, temp_db_path):
        """Test custom SQL queries"""
        # Save jobs first
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", None)
        
        # Test simple SELECT query
        results = query_jobs_from_duckdb(
            temp_db_path, 
            "test_jobs",
            "SELECT job_title, employer_name FROM test_jobs WHERE minimum_salary > 50000"
        )
        
        # Should return jobs with salary > 50000
        assert len(results) == 2  # Jobs 1 and 2 have salary > 50000
        # Note: The query doesn't include minimum_salary in SELECT, so we can't check it
        job_titles = [job['job_title'] for job in results]
        assert 'Python Developer' in job_titles
        assert 'Data Scientist' in job_titles
        
        # Test COUNT query
        count_results = query_jobs_from_duckdb(
            temp_db_path,
            "test_jobs", 
            "SELECT COUNT(*) as job_count FROM test_jobs"
        )
        assert count_results[0]['job_count'] == 3
    
    def test_get_job_statistics(self, sample_jobs, temp_db_path):
        """Test getting job statistics"""
        # Save jobs first
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", None)
        
        # Get statistics
        stats = get_job_statistics(temp_db_path, "test_jobs")
        
        # Verify statistics
        assert stats['total_jobs'] == 3
        assert stats['jobs_with_salary'] == 2  # Only 2 jobs have salary info
        assert stats['unique_employers'] == 2  # 2 unique employers
        
        # Check salary statistics
        assert stats['avg_min_salary'] == 55000.0  # (50000 + 60000) / 2
        assert stats['avg_max_salary'] == 75000.0  # (70000 + 80000) / 2
        
        # Check top employers
        assert len(stats['top_employers']) == 2
        # Test Company 1 should have 2 jobs, Test Company 2 should have 1 job
        employer_counts = dict(stats['top_employers'])
        assert employer_counts['Test Company 1'] == 2
        assert employer_counts['Test Company 2'] == 1
    
    def test_get_job_statistics_empty_table(self, temp_db_path):
        """Test getting statistics from empty table"""
        # Create empty table
        save_jobs_to_duckdb([], temp_db_path, "test_jobs", "reed", None)
        
        # Get statistics
        stats = get_job_statistics(temp_db_path, "test_jobs")
        
        # Verify empty statistics
        assert stats.get('total_jobs', 0) == 0
        assert stats.get('jobs_with_salary', 0) == 0
        assert stats.get('unique_employers', 0) == 0
        assert stats.get('top_employers', []) == []
    
    def test_get_job_statistics_nonexistent_table(self, temp_db_path):
        """Test getting statistics from non-existent table"""
        # Should return empty dict, not raise exception
        stats = get_job_statistics(temp_db_path, "nonexistent_table")
        assert stats == {}
    
    def test_data_source_parameter(self, sample_jobs, temp_db_path):
        """Test that data_source parameter is used correctly"""
        # Save jobs with custom data source
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "custom_source", None)
        
        # Load jobs and verify data source
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        for job in loaded_jobs:
            assert job['data_source'] == 'custom_source'
    
    def test_api_parameters_json_serialization(self, sample_jobs, temp_db_path):
        """Test that API parameters are properly serialized to JSON"""
        api_params = {
            'keywords': 'python',
            'location': 'London',
            'salary_min': 50000,
            'complex_param': {'nested': 'value', 'list': [1, 2, 3]}
        }
        
        # Save jobs with complex API parameters
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", api_params)
        
        # Load jobs and verify JSON serialization
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        for job in loaded_jobs:
            assert job['api_parameters'] == json.dumps(api_params)
            # Verify we can deserialize it back
            deserialized = json.loads(job['api_parameters'])
            assert deserialized == api_params
    
    def test_null_handling(self, temp_db_path):
        """Test handling of null values in job data"""
        jobs_with_nulls = [
            {
                'job_id': 1,
                'employer_id': 101,
                'employer_name': 'Test Company',
                'employer_profile_id': None,
                'job_title': 'Test Job',
                'description': 'Test description',
                'location_name': 'Test Location',
                'minimum_salary': None,
                'maximum_salary': None,
                'yearly_minimum_salary': None,
                'yearly_maximum_salary': None,
                'currency': None,
                'salary_type': None,
                'contract_type': None,
                'job_type': None,
                'expiration_date': None,
                'external_url': None,
                'reed_url': None
            }
        ]
        
        # Save jobs with null values
        save_jobs_to_duckdb(jobs_with_nulls, temp_db_path, "test_jobs", "reed", None)
        
        # Load jobs and verify null handling
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        
        assert len(loaded_jobs) == 1
        job = loaded_jobs[0]
        
        # Verify that null values are preserved
        assert job['employer_profile_id'] is None
        assert job['minimum_salary'] is None
        assert job['maximum_salary'] is None
        assert job['currency'] is None
        assert job['contract_type'] is None
        assert job['external_url'] is None
    
    def test_concurrent_access(self, sample_jobs, temp_db_path):
        """Test that multiple operations can access the same database"""
        # Save jobs
        save_jobs_to_duckdb(sample_jobs, temp_db_path, "test_jobs", "reed", None)
        
        # Perform multiple operations
        loaded_jobs = load_jobs_from_duckdb(temp_db_path, "test_jobs")
        stats = get_job_statistics(temp_db_path, "test_jobs")
        query_results = query_jobs_from_duckdb(
            temp_db_path, 
            "test_jobs",
            "SELECT COUNT(*) as count FROM test_jobs"
        )
        
        # All operations should work
        assert len(loaded_jobs) == 3
        assert stats['total_jobs'] == 3
        assert query_results[0]['count'] == 3 