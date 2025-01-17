import httpx
import time
import asyncio
import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape_search

INPUT_FILEPATH = "intersect/data/facilitator.feather"


async def get_description(url: str) -> str | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await scrape_search(client, url)
            print(f"OK: {url}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

    parser = LexborHTMLParser(response.text)
    result = parser.css_first(".job__description")

    if result is None:
        return None

    return result.text().strip()


async def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    semaphore = asyncio.Semaphore(10)
    
    async with semaphore: 
        tasks = [get_description(url) for url in df["url"]]
        descriptions = await asyncio.gather(*tasks)
    
    df["description"] = descriptions
    return df


async def main():
    start_time = time.time()

    df = pd.read_feather(INPUT_FILEPATH)
    df = await get_descriptions(df)
    df.to_feather(INPUT_FILEPATH)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())
