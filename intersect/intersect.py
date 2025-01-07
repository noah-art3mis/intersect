import pandas as pd
import numpy as np
from embedding import get_embedding
from openai import OpenAI
from dotenv import load_dotenv


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


def intersect(db_filepath: str, input_text: str) -> pd.DataFrame:
    load_dotenv()
    v = get_embedding(OpenAI(), input_text)
    df = pd.read_feather(db_filepath)
    return similarity_search(df, v)
