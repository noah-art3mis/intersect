import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken


def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):

    def num_tokens_from_string(string: str, model="text-embedding-3-small") -> int:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    if num_tokens_from_string(text) > 8000:
        raise Exception("Text too long")

    res = client.embeddings.create(model=model, input=text, encoding_format="float")

    return res.data[0].embedding


def similarity_search(df: pd.DataFrame, embedding) -> pd.DataFrame:
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
    client = OpenAI()

    v = get_embedding(client, input_text)
    df = pd.read_feather(db_filepath)
    result = similarity_search(df, v)

    return result
