import pandas as pd
import numpy as np

# -   https://huggingface.co/dunzhang/stella_en_1.5B_v5
# -   https://huggingface.co/dunzhang/stella_en_400M_v5
# -   https://huggingface.co/intfloat/e5-mistral-7b-instruct
# -   https://huggingface.co/BAAI/bge-reranker-base


def similarity_search(df: pd.DataFrame, embedding: list[float]) -> pd.DataFrame:
    """ expects a df with a column called 'embedding' """
    
    df["score_semantic"] = df["embedding"].apply(lambda x: np.dot(embedding, x))
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