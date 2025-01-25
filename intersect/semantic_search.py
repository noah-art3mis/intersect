import pandas as pd
import numpy as np

# -   https://huggingface.co/dunzhang/stella_en_1.5B_v5
# -   https://huggingface.co/dunzhang/stella_en_400M_v5
# -   https://huggingface.co/intfloat/e5-mistral-7b-instruct
# -   https://huggingface.co/BAAI/bge-reranker-base


def similarity_search(df: pd.DataFrame, embedding: list[float]) -> pd.DataFrame:
    # chatgpt code not sure about this working properly

    df = df.copy()
    df["original_position"] = df.index

    df["similarity"] = df["embedding"].apply(lambda x: np.dot(embedding, x))
    sorted = df.sort_values("similarity", ascending=False).reset_index(drop=True)

    sorted["i_semantic"] = sorted.index

    sorted = sorted.merge(
        df[["original_position"]], left_on="original_position", right_index=True
    )

    sorted["delta_semantic"] = sorted["original_position"] - sorted["i_semantic"]
    return sorted


# def calculate_position_change(
#     sorted_df: pd.DataFrame, original_positions: pd.DataFrame, new_col_name: str
# ) -> pd.Series:
    
#     sorted_df = sorted_df.copy()
#     sorted_df = sorted_df.merge(
#         original_positions, left_on="original_position", right_index=True
#     )
#     sorted_df["position_change"] = (
#         sorted_df["original_position"] - sorted_df["new_position"]
#     )
#     return sorted_df["position_change"]


# def similarity_search(df: pd.DataFrame, embedding: list) -> pd.DataFrame:
#     df = df.copy()
#     df["i_relevance"] = df.index

#     # Calculate similarity
#     df["similarity"] = df["embedding"].apply(lambda x: np.dot(embedding, x))

#     # Sort by similarity
#     sorted_df = df.sort_values("similarity", ascending=False).reset_index(drop=True)
#     sorted_df["new_position"] = sorted_df.index

#     # Calculate position change
#     sorted_df["position_change"] = calculate_position_change(
#         sorted_df, df[["original_position"]], ""
#     )

#     return sorted_df


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
