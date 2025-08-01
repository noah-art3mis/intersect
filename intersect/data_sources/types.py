from dataclasses import dataclass
from typing import Optional, List, Any, Dict
from datetime import datetime
import hashlib


@dataclass
class IntersectJob:
    """
    Unified job type that serves as the interface between data sources and analysis layer.
    This type is designed to be converted into a dataframe for analysis.

    All data sources should convert their job data into this type before
    being processed by the analysis algorithms.
    """

    # Core job identification
    title: str
    description: str
    employer: str
    location: str
    intersect_id: Optional[str] = None  # Will be auto-generated from description hash

    # Salary information
    salary: Optional[str] = None
    minimum_salary: Optional[int] = None
    maximum_salary: Optional[int] = None
    currency: Optional[str] = None
    salary_type: Optional[str] = None

    # Job details
    contract_type: Optional[str] = None  # "permanent", "contract", "temp"
    job_type: Optional[str] = None  # full-time, part-time
    applications: Optional[int] = None

    # URLs and links
    url: Optional[str] = None

    # Dates
    posted_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

    # Data source tracking
    data_source: Optional[str] = None  # reed, theirstack

    # Analysis fields (added during processing)
    embedding: Optional[List[float]] = None

    # Scoring fields (added during analysis)
    rank_lexical: Optional[int] = None
    score_lexical: Optional[float] = None

    rank_semantic: Optional[int] = None
    score_semantic: Optional[float] = None
    delta_semantic: Optional[int] = None

    rank_reranker: Optional[int] = None
    score_reranker: Optional[float] = None

    cluster_kmeans: Optional[int] = None
    cluster_hdbscan: Optional[int] = None

    # Additional metadata (for extensibility)
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for dataframe conversion"""
        return {
            "intersect_id": self.intersect_id,
            "title": self.title,
            "description": self.description,
            "employer": self.employer,
            "location": self.location,
            "salary": self.salary,
            "minimum_salary": self.minimum_salary,
            "maximum_salary": self.maximum_salary,
            "currency": self.currency,
            "salary_type": self.salary_type,
            "contract_type": self.contract_type,
            "job_type": self.job_type,
            "applications": self.applications,
            "url": self.url,
            "posted_date": self.posted_date,
            "expiration_date": self.expiration_date,
            "data_source": self.data_source,
            "embedding": self.embedding,
            "rank_lexical": self.rank_lexical,
            "score_lexical": self.score_lexical,
            "rank_semantic": self.rank_semantic,
            "score_semantic": self.score_semantic,
            "delta_semantic": self.delta_semantic,
            "rank_reranker": self.rank_reranker,
            "score_reranker": self.score_reranker,
            "cluster_kmeans": self.cluster_kmeans,
            "cluster_hdbscan": self.cluster_hdbscan,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntersectJob":
        """Create IntersectJob from dictionary"""
        return cls(**data)

    @classmethod
    def get_display_columns(cls) -> dict:
        """Get display column mapping for IntersectJob fields"""
        return {
            "title": "Job Title",
            "employer": "Company",
            "location": "Location",
            "applications": "Applicants",
            "salary": "Salary",
            "expiration_date": "Expires",
            "posted_date": "Posted",
            "description": "Description",
            "url": "URL",
        }

    def __post_init__(self):
        """Validate required fields after initialization and generate ID if needed"""
        if not self.title:
            raise ValueError("title is required")
        if not self.description:
            raise ValueError("description is required")
        if not self.data_source:
            raise ValueError("data_source is required")

        # Generate intersect_id from description hash if not provided
        if not self.intersect_id:
            # Create a hash of the description
            description_hash = hashlib.md5(self.description.encode("utf-8")).hexdigest()
            self.intersect_id = description_hash
