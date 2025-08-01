import pandas as pd
import streamlit as st
import hdbscan
import logging
import time
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def cluster_kmeans(
    df: pd.DataFrame, col_name: str, n_clusters: int = 3
) -> pd.DataFrame:
    """Add KMeans clusters to data"""
    logger.info(
        f"Starting KMeans clustering on {len(df)} samples using {col_name} coordinates with {n_clusters} clusters"
    )
    start_time = time.time()

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(df[[f"{col_name}1", f"{col_name}2"]])
    df["Cluster"] = clusters

    elapsed_time = time.time() - start_time
    logger.info(f"KMeans completed in {elapsed_time:.2f} seconds")
    logger.info(f"Cluster distribution: {pd.Series(clusters).value_counts().to_dict()}")

    return df


def cluster_hdbscan(
    df: pd.DataFrame, col_name: str, min_cluster_size: int = 5
) -> pd.DataFrame:
    """Add HDBSCAN clusters to data"""
    logger.info(
        f"Starting HDBSCAN clustering on {len(df)} samples using {col_name} coordinates with min_cluster_size={min_cluster_size}"
    )
    start_time = time.time()

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    clusters = clusterer.fit_predict(df[[f"{col_name}1", f"{col_name}2"]])
    df["Cluster"] = clusters

    elapsed_time = time.time() - start_time
    logger.info(f"HDBSCAN completed in {elapsed_time:.2f} seconds")
    logger.info(
        f"Number of clusters found: {len(set(clusters)) - (1 if -1 in clusters else 0)}"
    )
    logger.info(f"Number of noise points: {sum(clusters == -1)}")
    logger.info(f"Cluster distribution: {pd.Series(clusters).value_counts().to_dict()}")

    return df
