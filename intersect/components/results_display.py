import streamlit as st
import pandas as pd
import numpy as np
import logging
from utils.embedding import get_embedding
from algorithms.semantic_search import similarity_search
from utils.utils import add_index
from algorithms.lexical_search import lexical_search
from algorithms.rerank import rerank_cohere
from openai import OpenAI
from config.constants import DISPLAY_COLUMNS
from algorithms.wordcloud import render_wordcloud
from algorithms.pca import render_cluster_visualization

def render_original_results(df: pd.DataFrame) -> None:
    _display_df = df.rename(columns=DISPLAY_COLUMNS)
    st.dataframe(_display_df[DISPLAY_COLUMNS.values()])


def process_search(df: pd.DataFrame, input_text: str) -> None:
    # this code has a bunch of side effects on the df


    df['salary'] = df.apply(format_salary, axis=1)
    # df['days_ago'] = df.apply(calculate_days_ago, axis=1)
    
    openai_client = OpenAI()
    input_embedding = get_embedding(openai_client, input_text)

    if input_embedding is None:
        raise ValueError("Failed to generate embedding.")


    with st.spinner():
        render_wordcloud(df)


    st.write("### Most relevant (original)")
    with st.spinner():
        render_original_results(df)

    st.write("### Most relevant (lexical search)")
    with st.spinner():
        display_cols = {"i_lexical": "i_lexical", "score_lexical": "score_lexical"}
        display_cols.update(DISPLAY_COLUMNS)
        process_lexical_search(df, input_text)

    st.write("### Best fit (semantic search)")
    with st.spinner():
        df = process_semantic_search(openai_client, df, input_text, input_embedding)
        df.sort_values(by="score_semantic", ascending=False, inplace=True)

    st.write("### Most interesting (semantic delta)")
    with st.spinner():
        df = process_semantic_delta(df)
        df.sort_values(by="delta_semantic", inplace=True)


    with st.spinner():
        render_cluster_visualization(df, input_text, input_embedding)


    st.write("### Reranker (cross-encoding)")
    with st.spinner():
        df = process_reranker_search(df, input_text)
        df.sort_values(by="score_reranker", ascending=False, inplace=True)
        st.dataframe(df[display_cols].head(5), hide_index=True)


def process_semantic_search(client: OpenAI, df: pd.DataFrame, input_text: str, input_embedding: list) -> pd.DataFrame:
    df = similarity_search(df, input_embedding)
    df = add_index(df, "score_semantic", "i_semantic")
    return df


def process_lexical_search(df: pd.DataFrame, input_text: str):
    df = lexical_search(input_text, df, "description")
    
    df.sort_values(by="score_lexical", ascending=False, inplace=True)
    display_cols = {"i_lexical": "i_lexical", "score_lexical": "score_lexical"}
    display_cols.update(DISPLAY_COLUMNS)
    st.dataframe(df[display_cols].head(5), hide_index=True)


def process_reranker_search(df: pd.DataFrame, input_text: str) -> pd.DataFrame:
    df = rerank_cohere(input_text, df)
    df = add_index(df, "score_reranker", "i_reranker")
    return df


def process_semantic_delta(df: pd.DataFrame) -> pd.DataFrame:
    df["delta_semantic"] = df["i_relevance"] - df["i_semantic"]
    return df


def format_salary(row: pd.Series, currency: str = "£") -> str:
    """Format salary information for display"""
    min_salary = row['minimum_salary']
    max_salary = row['maximum_salary']
    
    if min_salary is "" or max_salary is "":
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    if min_salary is None or max_salary is None:
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    if min_salary is np.nan or max_salary is np.nan:
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    return f"{currency}{min_salary:,} - {currency}{max_salary:,}"