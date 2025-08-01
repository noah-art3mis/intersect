import cohere
import os
import pandas as pd


# -   https://docs.cohere.com/docs/reranking-best-practices
# -   https://osanseviero.github.io/hackerllama/blog/posts/sentence_embeddings2conclusion
# -   https://huggingface.co/cross-encoder/ms-marco-TinyBERT-L-2
# -   https://www.answer.ai/posts/2024-09-16-rerankers.html
# -   cohere supports reranking for structured data


def rerank_cohere(query: str, _df: pd.DataFrame) -> pd.DataFrame:
    API_KEY = os.environ["COHERE_API_KEY"]
    MODEL_NAME = "rerank-v3.5"

    docs = _df["description"].tolist()
    co = cohere.Client(API_KEY)

    response = co.rerank(
        query=query,
        model=MODEL_NAME,
        documents=docs,
        # top_n=top_n,
    )

    # Create a mapping of description to score
    score_mapping = {}
    for result in response.results:
        score_mapping[result.index] = result.relevance_score

    # Add the score_reranker column to the original dataframe
    _df["score_reranker"] = _df.index.map(score_mapping)
    return _df
