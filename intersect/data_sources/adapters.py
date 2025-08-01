from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

from .types import IntersectJob
from .reed_types import ReedJob


def reed_job_to_intersect_job(reed_job: ReedJob) -> IntersectJob:
    """Convert ReedJob to IntersectJob"""
    return IntersectJob(
        title=reed_job.job_title,
        description=reed_job.description,
        employer=reed_job.employer_name,
        location=reed_job.location_name,
        salary=None,  # Will be calculated during preprocessing
        minimum_salary=reed_job.minimum_salary,
        maximum_salary=reed_job.maximum_salary,
        currency=reed_job.currency,
        salary_type=reed_job.salary_type,
        contract_type=reed_job.contract_type,
        job_type=reed_job.job_type,
        applications=reed_job.applications,
        url=reed_job.job_url,
        posted_date=None,  # Not available in Reed search results
        expiration_date=(
            datetime.fromisoformat(reed_job.expiration_date)
            if reed_job.expiration_date
            else None
        ),
        data_source=reed_job.data_source,
    )


def theirstack_job_to_intersect_job(job_dict: Dict[str, Any]) -> IntersectJob:
    """Convert Theirstack job dictionary to IntersectJob"""
    return IntersectJob(
        title=job_dict["title"],
        description=job_dict["description"],
        employer=job_dict["employer_name"],
        location=job_dict["location"],
        salary=job_dict.get("salary"),
        minimum_salary=None,  # Not available in theirstack data
        maximum_salary=None,  # Not available in theirstack data
        currency=job_dict.get("salary_currency"),
        salary_type=None,
        contract_type=None,
        job_type=None,
        applications=None,
        url=job_dict.get("url"),
        posted_date=(
            datetime.fromisoformat(job_dict["posted"])
            if job_dict.get("posted")
            else None
        ),
        expiration_date=None,
        data_source="theirstack",
        embedding=job_dict.get("embedding"),
    )


def reed_jobs_to_intersect_jobs(reed_jobs: List[ReedJob]) -> List[IntersectJob]:
    """Convert list of ReedJob objects to IntersectJob objects"""
    return [reed_job_to_intersect_job(job) for job in reed_jobs]


def theirstack_jobs_to_intersect_jobs(
    job_dicts: List[Dict[str, Any]]
) -> List[IntersectJob]:
    """Convert list of Theirstack job dictionaries to IntersectJob objects"""
    return [theirstack_job_to_intersect_job(job_dict) for job_dict in job_dicts]
