from dataclasses import dataclass
from typing import Optional


@dataclass
class ReedJob:
    """Data class to represent a job listing from Reed API"""

    job_id: int
    employer_name: str
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
    applications: Optional[int]
    job_url: Optional[str]
    data_source: str
