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

    results = []
    for result in response.results:
        results.append(
            {
                "score_reranker": result.relevance_score,
                "description": docs[result.index],
            }
        )

    df_lexical = pd.DataFrame(results)
    _df = _df.merge(df_lexical, how="left", on="description")
    return _df
