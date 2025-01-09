import pandas as pd
import numpy as np
from embedding import get_embedding
from openai import OpenAI

# -   https://huggingface.co/dunzhang/stella_en_1.5B_v5
# -   https://huggingface.co/dunzhang/stella_en_400M_v5
# -   https://huggingface.co/intfloat/e5-mistral-7b-instruct
# -   https://huggingface.co/BAAI/bge-reranker-base


def similarity_search(df: pd.DataFrame, embedding: list) -> pd.DataFrame:
    # chatgpt code not sure about this working properly

    df = df.copy()
    df["original_position"] = df.index

    df["similarity"] = df["embedding"].apply(lambda x: np.dot(embedding, x))
    sorted = df.sort_values("similarity", ascending=False).reset_index(drop=True)

    sorted["new_position"] = sorted.index

    sorted = sorted.merge(
        df[["original_position"]], left_on="original_position", right_index=True
    )

    sorted["position_change"] = sorted["original_position"] - sorted["new_position"]
    return sorted


def intersect(df: pd.DataFrame, input_text: str) -> pd.DataFrame:
    v = get_embedding(OpenAI(), input_text)
    result = similarity_search(df, v)
    formatted = format_columns(result)
    return formatted


def format_columns(df: pd.DataFrame) -> pd.DataFrame:

    df["rank"] = df.index + 1

    # reorder and drop columns
    df = df[
        [
            "rank",
            "title",
            "position_change",
            "similarity",
            "description",
            "url",
            "embedding",
        ]
    ]

    # rename columns
    df.columns = [
        "Rank",
        "Title",
        "Delta",
        "Similarity",
        "Description",
        "Link",
        "Vector",
    ]

    return df
