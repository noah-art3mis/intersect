import streamlit as st
import pandas as pd
from openai import OpenAI

from config.constants import TABLE_SIZE
from components.job_search import get_display_columns
from algorithms.semantic_search import similarity_search
from algorithms.lexical_search import lexical_search
from algorithms.wordcloud import render_wordcloud
from algorithms.pca import render_cluster_visualization
from algorithms.rerank import rerank_cohere
from utils.utils import add_index
from utils.embedding import get_input_embeddings, get_embedding

def process_search(df: pd.DataFrame, input_text: str, data_source: str = "reed") -> None:
    # this code has a bunch of side effects on the df

    openai_client = OpenAI()
    input_embedding = get_input_embeddings(openai_client, input_text)

    # with st.spinner():
    #     render_wordcloud(df)

    st.write("### Original ranking")
    with st.spinner():
        df.reset_index(inplace=True)
        df['index'] = df['index'] + 1
        display_df(df, {"index": "Rank O"}, data_source)

    st.write("### Most relevant (lexical search)")
    with st.spinner():
        process_lexical_search(df, input_text, data_source)

    st.write("### Most similar (semantic search)")
    with st.spinner():
        df = process_semantic_search(openai_client, df, input_embedding, data_source)

    st.write("### Most interesting (semantic delta)")
    with st.spinner():
        df = process_semantic_delta(df, data_source)
        df.sort_values(by="delta_semantic", inplace=True)

    st.write("### Reranker (cross-encoding)")
    with st.spinner():
        df = process_reranker_search(df, input_text, data_source)
          
    with st.spinner():
        render_cluster_visualization(df, input_text, input_embedding)   


def process_semantic_search(client: OpenAI, df: pd.DataFrame, input_embedding: list, data_source: str = "reed") -> pd.DataFrame:
    
    df['embedding'] = df['description'].apply(lambda x: get_embedding(client, x))
    df = similarity_search(df, input_embedding)
    df = add_index(df, "score_semantic", "i_semantic")
    df.sort_values(by="score_semantic", ascending=False, inplace=True)
    new_cols = {"score_semantic": "Rank S"}
    display_df(df, new_cols, data_source)
    return df



def process_lexical_search(df: pd.DataFrame, input_text: str, data_source: str = "reed"):
    df = lexical_search(input_text, df, "description")
    df.sort_values(by="score_lexical", ascending=False, inplace=True)
    new_cols = {"score_lexical": "Rank L"}
    display_df(df, new_cols, data_source)

def process_reranker_search(df: pd.DataFrame, input_text: str, data_source: str = "reed") -> pd.DataFrame:
    df = rerank_cohere(input_text, df)
    df = add_index(df, "score_reranker", "i_reranker")
    df.sort_values(by="score_reranker", ascending=False, inplace=True)
    new_cols = {"score_reranker": "Rank R"}
    display_df(df, new_cols, data_source)
    return df


def process_semantic_delta(df: pd.DataFrame, data_source: str = "reed") -> pd.DataFrame:
    df["delta_semantic"] = df["index"] - df["i_semantic"]
    df.sort_values(by="delta_semantic", inplace=True)
    new_cols = {"delta_semantic": "Rank D"}
    display_df(df, new_cols, data_source)
    return df

def display_df(df: pd.DataFrame, display_cols: dict, data_source: str = "reed") -> None:
    display_columns = get_display_columns(data_source)
    display_cols.update(display_columns)
    _df = df.rename(columns=display_cols)
    st.dataframe(_df[display_cols.values()].head(TABLE_SIZE), hide_index=True)