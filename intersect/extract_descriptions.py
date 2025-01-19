import time
import asyncio
import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape
from curl_cffi.requests import AsyncSession
from embedding import generate_embeddings

INPUT_FILEPATH = "intersect/data/law-ai.feather"
SEMAPHORE_LIMIT = 5


async def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async with AsyncSession() as client:
        tasks = [
            get_description(client, url, index, semaphore)
            for index, url in enumerate(df["url"])
        ]

        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

    # Sort results by the original index
    results.sort(key=lambda x: x[0])

    # TODO add incremental saving
    # TODO add embedding generation in parallel

    # Assign descriptions back to the DataFrame
    descriptions = [desc for _, desc in results]
    df["description"] = descriptions

    return df


async def get_description(
    client: AsyncSession, url: str, index: int, semaphore: asyncio.Semaphore
) -> tuple[int, str | None]:

    response = await scrape(client, url, semaphore)

    if response is None:
        return index, None

    parser = LexborHTMLParser(response.text)
    result = parser.css_first(".job__description")

    if result is None:
        return index, None

    return index, result.text().strip()


async def main():
    start_time = time.time()

    df = pd.read_feather(INPUT_FILEPATH)

    try:
        df = await get_descriptions(df)
    except Exception as e:
        print(f"Error occurred during scraping: {e}")

    df = generate_embeddings(df)

    df.to_feather(INPUT_FILEPATH)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
