from rich import print
import re
import json
from openai import OpenAI
import pandas as pd

# https://plainenglish.io/blog/improving-rag-using-llms-as-re-ranking-agents
# https://arxiv.org/abs/2304.09542
# https://arxiv.org/html/2406.12433v2
# https://github.com/castorini/rank_llm/
# https://blog.reachsumit.com/posts/2023/12/prompting-llm-for-ranking/
# https://cookbook.openai.com/examples/search_reranking_with_cross-encoders


def build_prompt(query: str, snippets: str) -> list[dict]:
    with open("intersect/data/prompt.txt", "r") as f:
        content = f.read()

    content = re.sub(r"{{query}}", query, content)
    content = re.sub(r"{{variable}}", snippets, content)

    return [
        {"role": "user", "content": content},
    ]


def permutation_openai(query: str, df: pd.DataFrame, model="gpt-4o-mini", top_k=10):

    client = OpenAI()

    df = df.sort_values("i_relevance", ascending=False)

    snippets = ""
    for index, row in df[:top_k].iterrows():
        snippets += f"""
            <item_{index}>
                index: {row['i_relevance']}
                title: {row["title"]}
                description: {row["description"]}
            </item_{index}>
                """

    prompt = build_prompt(query, snippets)
    completion = client.chat.completions.create(
        model=model,
        messages=prompt,  # type: ignore
        temperature=0,
    )

    results = completion.choices[0].message.content

    if results is None:
        raise Exception("No results")

    return postprocess_permutation(results)


def postprocess_permutation(response: str) -> pd.DataFrame:

    cleaned_text = re.sub(
        r"<ranking_criteria>.*?</ranking_criteria>", "", response, flags=re.DOTALL
    )

    cleaned_text = re.sub("new_rank", "i_permutation", cleaned_text)
    cleaned_text = re.sub("index", "i_relevance", cleaned_text)
    
    data = json.loads(cleaned_text.strip())
    df = pd.DataFrame(data)
    df = df.sort_values("i_permutation")

    return df