from pydantic import BaseModel
import json
from rich import print
from openai import OpenAI
import pandas as pd

# https://plainenglish.io/blog/improving-rag-using-llms-as-re-ranking-agents
# https://arxiv.org/abs/2304.09542
# https://arxiv.org/html/2406.12433v2
# https://github.com/castorini/rank_llm/
# https://github.com/castorini/rank_llm/
# https://blog.reachsumit.com/posts/2023/12/prompting-llm-for-ranking/
# https://cookbook.openai.com/examples/search_reranking_with_cross-encoders


class PermutationResult(BaseModel):
    new_rank: int
    old_rank: int
    description: str


class PermutationResults(BaseModel):
    results: list[PermutationResult]


def build_prompt(query: str, snippets: list[dict]) -> list[dict]:
    content = f"I will provide you with passages. Rank the passages based on their relevance to query: {query}. Respond with a list of json objects and nothing else. these objects should have the fields: `title`, `old_rank` and `new_rank`. Order results by `new_rank`.\n\n###\n\nPassages:\n\n"

    for snippet in snippets:
        content = content + f"* {str(snippet)}\n\n"

    return [
        {
            "role": "developer",
            "content": "You are RankGPT, an assistant that can rank passages based on their relevance to the query.",
        },
        {"role": "user", "content": content},
    ]


def permutation_openai(query: str, snippets: list[dict], model="gpt-4o-mini", top_k=10):

    client = OpenAI()

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=build_prompt(query, snippets),  # type: ignore
        temperature=0,
        response_format=PermutationResults,
    )

    results = completion.choices[0].message.parsed

    if results is None:
        raise Exception("No results")

    return postprocess_permutation(results, top_k=top_k)


def postprocess_permutation(response: PermutationResults, top_k=10) -> pd.DataFrame:

    data = [result.model_dump() for result in response.results]
    df = pd.DataFrame(data)
    df = df.sort_values("new_rank")

    df = df[["new_rank", "old_rank", "description"]]
    return df
