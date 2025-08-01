import streamlit as st
import pandas as pd
from openai import OpenAI
import logging

from config.constants import TABLE_SIZE
from components.job_search import get_display_columns
from algorithms.semantic_search import similarity_search
from algorithms.lexical_search import lexical_search
from algorithms.wordcloud import render_wordcloud
from algorithms.visualizations import render_umap_hdbscan
from algorithms.clustering import cluster_hdbscan, cluster_kmeans
from algorithms.rerank import rerank_cohere
from algorithms.dimensionality_reduction import umap_df
from utils.utils import add_index, add_you
from utils.embedding import get_input_embeddings, get_embedding


def process_search(
    df: pd.DataFrame, input_text: str, data_source: str = "reed"
) -> None:
    # this code has a bunch of side effects on the df

    openai_client = OpenAI()
    input_embedding = get_input_embeddings(openai_client, input_text)

    if "embedding" not in df.columns:
        with st.spinner():
            logging.info("Embeddings not found in data. Generating...")
            df["embedding"] = df["description"].apply(
                lambda x: get_embedding(openai_client, x)
            )

    # Show the plot first
    st.write("### Cluster Visualization")
    with st.spinner("📊 Creating cluster visualization..."):
        df_you = add_you(df.copy(), input_text, input_embedding)  # type: ignore
        # df_pca = pca_df(df_you, "embedding")
        df_umap = umap_df(df_you, "embedding")

        # render_pca_kmeans(df_pca.copy())
        # render_umap_kmeans(df_umap.copy())
        # render_pca_hdbscan(df_pca.copy())

        st.caption("UMAP + HDBSCAN")
        render_umap_hdbscan(df_umap.copy())

    # with st.spinner():
    #     render_wordcloud(df)

    st.write("### Original ranking")
    with st.spinner():
        df.reset_index(inplace=True)
        df["index"] = df["index"] + 1
        display_df(df, {"index": "Rank O"}, data_source)

    with st.spinner():
        st.write("### Most relevant")
        st.caption("Lexical search (BM25)")
        process_lexical_search(df, input_text, data_source)

    with st.spinner():
        st.write("### Most similar")
        st.caption("Semantic search (embeddings-3-small)")
        df = process_semantic_search(openai_client, df, input_embedding, data_source)

    with st.spinner():
        st.write("### Most interesting")
        st.caption("Semantic delta (change in rank from lexical to semantic)")
        df = process_semantic_delta(df, data_source)
        df.sort_values(by="delta_semantic", inplace=True)

    with st.spinner():
        st.write("### Reranking")
        st.caption("Cross-encoding (Cohere)")
        df = process_reranker_search(df, input_text, data_source)


def process_semantic_search(
    client: OpenAI, df: pd.DataFrame, input_embedding: list, data_source: str = "reed"
) -> pd.DataFrame:

    # Embeddings are already generated, just compute similarity
    df = similarity_search(df, input_embedding)
    df = add_index(df, "score_semantic", "i_semantic")
    df.sort_values(by="score_semantic", ascending=False, inplace=True)
    new_cols = {"score_semantic": "Rank S"}
    display_df(df, new_cols, data_source)
    return df


def process_lexical_search(
    df: pd.DataFrame, input_text: str, data_source: str = "reed"
):
    df = lexical_search(input_text, df, "description")
    df.sort_values(by="score_lexical", ascending=False, inplace=True)
    new_cols = {"score_lexical": "Rank L"}
    display_df(df, new_cols, data_source)


def process_reranker_search(
    df: pd.DataFrame, input_text: str, data_source: str = "reed"
) -> pd.DataFrame:
    df = rerank_cohere(input_text, df)
    df = add_index(df, "score_reranker", "i_reranker")
    df.sort_values(by="score_reranker", ascending=False, inplace=True)
    new_cols = {"score_reranker": "Rank R"}
    display_df(df, new_cols, data_source)
    return df


def process_semantic_delta(df: pd.DataFrame, data_source: str = "reed") -> pd.DataFrame:
    df["delta_semantic"] = df["index"] - df["i_semantic"]
    df.sort_values(by="delta_semantic", ascending=False, inplace=True)
    new_cols = {"delta_semantic": "Rank D"}
    display_df(df, new_cols, data_source)
    return df


def display_df(df: pd.DataFrame, display_cols: dict, data_source: str = "reed") -> None:
    display_columns = get_display_columns(data_source)
    display_cols.update(display_columns)
    _df = df.rename(columns=display_cols)
    st.dataframe(_df[display_cols.values()].head(TABLE_SIZE), hide_index=True)
