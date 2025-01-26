import pandas as pd
import numpy as np

# -   https://huggingface.co/dunzhang/stella_en_1.5B_v5
# -   https://huggingface.co/dunzhang/stella_en_400M_v5
# -   https://huggingface.co/intfloat/e5-mistral-7b-instruct
# -   https://huggingface.co/BAAI/bge-reranker-base


# def similarity_search(df: pd.DataFrame, embedding: list[float]) -> pd.DataFrame:
#     # chatgpt code not sure about this working properly

#     df = df.copy()
#     df["original_position"] = df.index

#     df["similarity"] = df["embedding"].apply(lambda x: np.dot(embedding, x))
#     sorted = df.sort_values("similarity", ascending=False).reset_index(drop=True)

#     sorted["i_semantic"] = sorted.index

#     sorted = sorted.merge(
#         df[["original_position"]], left_on="original_position", right_index=True
#     )

#     sorted["delta_semantic"] = sorted["original_position"] - sorted["i_semantic"]
#     return sorted


def similarity_search(df: pd.DataFrame, embedding: list[float]) -> pd.DataFrame:
    """Adds a column with the semantic search results and one with the displacement"""
    
    df["similarity"] = df["embedding"].apply(lambda x: np.dot(embedding, x))
    df = df.sort_values(by="similarity", ascending=False)
    df = df.reset_index(drop=True)
    df["i_semantic"] = df.index

    df["delta_semantic"] = df["i_relevance"] - df["i_semantic"]
    return df


# def format_columns(df: pd.DataFrame) -> pd.DataFrame:

#     # df["rank"] = df.index
#     df["rank"] = df.index + 1

#     # reorder and drop columns
#     df = df[
#         [
#             "rank",
#             "title",
#             "position_change",
#             "similarity",
#             "description",
#             "url",
#             "embedding",
#         ]
#     ]

#     # rename columns
#     df.columns = [
#         "Rank",
#         "Title",
#         "Delta",
#         "Similarity",
#         "Description",
#         "Link",
#         "Vector",
#     ]

#     return df
