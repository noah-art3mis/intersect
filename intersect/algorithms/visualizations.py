import pandas as pd
import altair as alt
import streamlit as st
import logging

from utils.utils import add_you
from algorithms.dimensionality_reduction import pca_df, umap_df
from algorithms.clustering import cluster_kmeans, cluster_hdbscan

logger = logging.getLogger(__name__)


def get_chart(df: pd.DataFrame, x_col: str, y_col: str) -> alt.Chart:
    """Create Altair chart for visualization"""
    chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x=alt.X(f"{x_col}:Q", scale=alt.Scale(zero=False)),
            y=alt.Y(f"{y_col}:Q", scale=alt.Scale(zero=False)),
            color="Cluster:N",
            tooltip=alt.Tooltip(
                [
                    "title:N",
                    "days_ago:Q",
                    "score_semantic:Q",
                    "description:N",
                ],
                # format=".2f", # coerces all fields
            ),
        )
        .properties(width="container", height=400)
    )

    return chart


def render_cluster_visualization(
    df: pd.DataFrame, input_text: str, input_embedding: list[float]
) -> None:
    st.write("### Cluster Visualization")
    st.write("Hover over items to see more details")

    df_you = add_you(df.copy(), input_text, input_embedding)  # type: ignore
    # df_pca = pca_df(df_you, "embedding")
    df_umap = umap_df(df_you, "embedding")

    # render_pca_kmeans(df_pca.copy())
    # render_umap_kmeans(df_umap.copy())
    # render_pca_hdbscan(df_pca.copy())
    render_umap_hdbscan(df_umap.copy())


def render_pca_kmeans(df_pca: pd.DataFrame) -> None:
    """Render PCA + KMeans visualization"""
    logger.info("Generating PCA + KMeans visualization")
    st.write("#### PCA + KMeans (3 clusters)")
    df_clustered = cluster_kmeans(df_pca, "PC", n_clusters=3)
    # Convert Cluster column to string to avoid dtype incompatibility
    df_clustered["Cluster"] = df_clustered["Cluster"].astype(str)
    df_clustered.loc[df_clustered["title"] == "Your text", "Cluster"] = " You"
    chart = get_chart(df_clustered, "PC1", "PC2")
    st.altair_chart(chart, use_container_width=True)


def render_umap_kmeans(df_umap: pd.DataFrame) -> None:
    """Render UMAP + KMeans visualization"""
    logger.info("Generating UMAP + KMeans visualization")
    st.write("#### UMAP + KMeans (3 clusters)")
    df_clustered = cluster_kmeans(df_umap, "UMAP", n_clusters=3)
    # Convert Cluster column to string to avoid dtype incompatibility
    df_clustered["Cluster"] = df_clustered["Cluster"].astype(str)
    df_clustered.loc[df_clustered["title"] == "Your text", "Cluster"] = " You"
    chart = get_chart(df_clustered, "UMAP1", "UMAP2")
    st.altair_chart(chart, use_container_width=True)


def render_pca_hdbscan(df_pca: pd.DataFrame) -> None:
    """Render PCA + HDBSCAN visualization"""
    logger.info("Generating PCA + HDBSCAN visualization")
    st.write("#### PCA + HDBSCAN")
    df_clustered = cluster_hdbscan(df_pca, "PC", min_cluster_size=5)
    # Convert Cluster column to string to avoid dtype incompatibility
    df_clustered["Cluster"] = df_clustered["Cluster"].astype(str)
    df_clustered.loc[df_clustered["title"] == "Your text", "Cluster"] = " You"
    chart = get_chart(df_clustered, "PC1", "PC2")
    st.altair_chart(chart, use_container_width=True)


def render_umap_hdbscan(df_umap: pd.DataFrame) -> None:
    """Render UMAP + HDBSCAN visualization"""
    logger.info("Generating UMAP + HDBSCAN visualization")
    df_clustered = cluster_hdbscan(df_umap, "UMAP", min_cluster_size=5)
    # Convert Cluster column to string to avoid dtype incompatibility
    df_clustered["Cluster"] = df_clustered["Cluster"].astype(str)
    df_clustered.loc[df_clustered["title"] == "Your text", "Cluster"] = " You"
    chart = get_chart(df_clustered, "UMAP1", "UMAP2")
    st.altair_chart(chart, use_container_width=True)
