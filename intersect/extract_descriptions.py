from dotenv import load_dotenv
from openai import OpenAI
import time
import asyncio
import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape
from curl_cffi.requests import AsyncSession
from embedding import get_embedding

INPUT_FILEPATH = "intersect/data/leadership.feather"
SEMAPHORE_LIMIT = 5


async def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:

    load_dotenv()
    openai_client = OpenAI()
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async with AsyncSession() as client:
        tasks = [
            get_description(client, url, index, semaphore, openai_client)
            for index, url in enumerate(df["url"])
        ]

        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

    # Sort results by the original index
    results.sort(key=lambda x: x[0])

    temp_df = pd.DataFrame(results, columns=["index", "description", "embedding"])
    df["description"] = temp_df["description"]
    df["embedding"] = temp_df["embedding"]

    # TODO add incremental saving

    return df


async def get_description(
    client: AsyncSession,
    url: str,
    index: int,
    semaphore: asyncio.Semaphore,
    ai_client: OpenAI,
) -> tuple[int, str | None, list[float] | None]:

    response = await scrape(client, url, semaphore)

    if response is None:
        return index, None, None

    parser = LexborHTMLParser(response.text)
    result = parser.css_first(".job__description")

    if result is None:
        return index, None, None

    result_string = result.text().strip()
    embedding = get_embedding(ai_client, result_string)

    return index, result_string, embedding


async def main():
    start_time = time.time()

    df = pd.read_feather(INPUT_FILEPATH)

    try:
        df = await get_descriptions(df)
    except Exception as e:
        print(f"Error occurred during scraping: {e}")

    df.to_feather(INPUT_FILEPATH)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
