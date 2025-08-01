import pandas as pd
import streamlit as st
import umap.umap_ as umap
import logging
import time
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


def pca_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Apply PCA dimensionality reduction"""
    logger.info(f"Starting PCA dimensionality reduction on {len(df)} samples")
    start_time = time.time()

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[col].tolist())
    pca_df = pd.DataFrame(principal_components, columns=["PC1", "PC2"])  # type: ignore

    elapsed_time = time.time() - start_time
    logger.info(f"PCA completed in {elapsed_time:.2f} seconds")
    logger.info(f"Explained variance ratio: {pca.explained_variance_ratio_}")

    return pd.concat([df, pca_df], axis=1)


def umap_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Apply UMAP dimensionality reduction using official parameters"""
    # Based on https://umap-learn.readthedocs.io/en/latest/
    logger.info(f"Starting UMAP dimensionality reduction on {len(df)} samples")
    start_time = time.time()

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=15,  # Default from documentation
        min_dist=0.1,  # Default from documentation
        metric="euclidean",  # Default metric
        random_state=42,
        verbose=False,
    )
    umap_components = reducer.fit_transform(df[col].tolist())
    umap_df = pd.DataFrame(umap_components, columns=["UMAP1", "UMAP2"])  # type: ignore

    elapsed_time = time.time() - start_time
    logger.info(f"UMAP completed in {elapsed_time:.2f} seconds")

    return pd.concat([df, umap_df], axis=1)
