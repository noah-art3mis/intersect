"""
DuckDB storage utilities for job data
"""

import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import duckdb
import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)


def ensure_data_directory():
    """Ensure the data/duckdb directory exists"""
    data_dir = os.path.join(os.path.dirname(__file__), "data", "duckdb")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def save_jobs_to_duckdb(jobs: List[Dict[str, Any]], db_path: str, table_name: str, data_source: str, api_params: Optional[Dict[str, Any]] = None) -> None:
    """
    Save a list of job dictionaries to DuckDB
    
    Args:
        jobs: List of job dictionaries to save
        db_path: Path to the DuckDB database file (will be saved in intersect/data/duckdb/)
        table_name: Name of the table to create/overwrite
        data_source: Source of the job data (e.g., 'reed')
        api_params: Dictionary of API parameters used for the search
    """
    if not jobs:
        logger.warning("No jobs to save")
        return
    
    # Ensure data directory exists and get full path
    data_dir = ensure_data_directory()
    full_db_path = os.path.join(data_dir, db_path)
    
    # Add metadata fields to each job
    jobs_with_metadata = []
    for job in jobs:
        job_with_metadata = job.copy()
        job_with_metadata['data_source'] = data_source
        job_with_metadata['api_parameters'] = json.dumps(api_params) if api_params else None
        job_with_metadata['created_at'] = datetime.now().isoformat()
        jobs_with_metadata.append(job_with_metadata)
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(jobs_with_metadata)
    
    # Connect to DuckDB and save the data
    try:
        with duckdb.connect(full_db_path) as conn:
            # Create or replace the table
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            
            # Log the results
            result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            if result:
                logger.info(f"Successfully saved {result[0]} jobs to {full_db_path}.{table_name}")
            else:
                logger.warning("Could not get job count from database")
            
            # Show table schema
            schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
            logger.info(f"Table schema: {schema}")
            
    except Exception as e:
        logger.error(f"Error saving jobs to DuckDB: {e}")
        raise


def load_jobs_from_duckdb(db_path: str, table_name: str) -> List[Dict[str, Any]]:
    """
    Load jobs from DuckDB back to dictionaries
    
    Args:
        db_path: Path to the DuckDB database file (will be loaded from intersect/data/duckdb/)
        table_name: Name of the table to read from
        
    Returns:
        List of job dictionaries
    """
    # Ensure data directory exists and get full path
    data_dir = ensure_data_directory()
    full_db_path = os.path.join(data_dir, db_path)
    
    try:
        with duckdb.connect(full_db_path) as conn:
            # Check if table exists
            tables = conn.execute("SHOW TABLES").fetchall()
            table_names = [table[0] for table in tables]
            
            if table_name not in table_names:
                logger.warning(f"Table {table_name} not found in {full_db_path}")
                return []
            
            # Load data
            df = conn.execute(f"SELECT * FROM {table_name}").df()
            
            # Convert back to dictionaries
            jobs = []
            for _, row in df.iterrows():
                # Helper function to safely convert values
                def safe_int(value):
                    if pd.isna(value):
                        return None
                    return int(value)
                
                def safe_str(value):
                    if pd.isna(value):
                        return None
                    return str(value)
                
                job_dict = {
                    'job_id': safe_int(row['job_id']),
                    'employer_id': safe_int(row['employer_id']),
                    'employer_name': safe_str(row['employer_name']),
                    'employer_profile_id': safe_int(row['employer_profile_id']),
                    'job_title': safe_str(row['job_title']),
                    'description': safe_str(row['description']),
                    'location_name': safe_str(row['location_name']),
                    'minimum_salary': safe_int(row['minimum_salary']),
                    'maximum_salary': safe_int(row['maximum_salary']),
                    'yearly_minimum_salary': safe_int(row['yearly_minimum_salary']),
                    'yearly_maximum_salary': safe_int(row['yearly_maximum_salary']),
                    'currency': safe_str(row['currency']),
                    'salary_type': safe_str(row['salary_type']),
                    'contract_type': safe_str(row['contract_type']),
                    'job_type': safe_str(row['job_type']),
                    'expiration_date': safe_str(row['expiration_date']),
                    'external_url': safe_str(row['external_url']),
                    'reed_url': safe_str(row['reed_url']),
                    'data_source': safe_str(row['data_source']),
                    'api_parameters': safe_str(row['api_parameters']),
                    'created_at': safe_str(row['created_at'])
                }
                jobs.append(job_dict)
            
            logger.info(f"Successfully loaded {len(jobs)} jobs from {db_path}.{table_name}")
            return jobs
            
    except Exception as e:
        logger.error(f"Error loading jobs from DuckDB: {e}")
        raise


def query_jobs_from_duckdb(db_path: str, table_name: str, query: str) -> List[Dict[str, Any]]:
    """
    Execute a custom SQL query on the jobs table
    
    Args:
        db_path: Path to the DuckDB database file (will be loaded from intersect/data/duckdb/)
        table_name: Name of the table to query
        query: SQL query to execute
        
    Returns:
        List of job dictionaries matching the query
    """
    # Ensure data directory exists and get full path
    data_dir = ensure_data_directory()
    full_db_path = os.path.join(data_dir, db_path)
    
    try:
        with duckdb.connect(full_db_path) as conn:
            # Execute the query
            df = conn.execute(query).df()
            
            # Convert to list of dictionaries
            results = df.to_dict('records')
            logger.info(f"Query returned {len(results)} results")
            return results
            
    except Exception as e:
        logger.error(f"Error executing query on DuckDB: {e}")
        raise


def get_job_statistics(db_path: str, table_name: str) -> Dict[str, Any]:
    """
    Get basic statistics about jobs in the database
    
    Args:
        db_path: Path to the DuckDB database file (will be loaded from intersect/data/duckdb/)
        table_name: Name of the table to analyze
        
    Returns:
        Dictionary with job statistics
    """
    # Ensure data directory exists and get full path
    data_dir = ensure_data_directory()
    full_db_path = os.path.join(data_dir, db_path)
    
    try:
        with duckdb.connect(full_db_path) as conn:
            # Check if table exists
            tables = conn.execute("SHOW TABLES").fetchall()
            table_names = [table[0] for table in tables]
            
            if table_name not in table_names:
                logger.warning(f"Table {table_name} not found in {full_db_path}")
                return {}
            
            # Get basic statistics
            stats = {}
            
            # Total jobs
            total_result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            stats['total_jobs'] = total_result[0] if total_result else 0
            
            # Jobs with salary info
            salary_result = conn.execute(f"""
                SELECT COUNT(*) FROM {table_name} 
                WHERE minimum_salary IS NOT NULL OR maximum_salary IS NOT NULL
            """).fetchone()
            stats['jobs_with_salary'] = salary_result[0] if salary_result else 0
            
            # Unique employers
            employers_result = conn.execute(f"""
                SELECT COUNT(DISTINCT employer_name) FROM {table_name}
            """).fetchone()
            stats['unique_employers'] = employers_result[0] if employers_result else 0
            
            # Average salary
            avg_salary_result = conn.execute(f"""
                SELECT 
                    AVG(minimum_salary) as avg_min,
                    AVG(maximum_salary) as avg_max
                FROM {table_name} 
                WHERE minimum_salary IS NOT NULL OR maximum_salary IS NOT NULL
            """).fetchone()
            
            if avg_salary_result:
                stats['avg_min_salary'] = avg_salary_result[0]
                stats['avg_max_salary'] = avg_salary_result[1]
            
            # Top employers
            top_employers_result = conn.execute(f"""
                SELECT employer_name, COUNT(*) as job_count
                FROM {table_name} 
                GROUP BY employer_name 
                ORDER BY job_count DESC 
                LIMIT 5
            """).fetchall()
            
            stats['top_employers'] = [(row[0], row[1]) for row in top_employers_result]
            
            return stats
            
    except Exception as e:
        logger.error(f"Error getting job statistics from DuckDB: {e}")
        raise 