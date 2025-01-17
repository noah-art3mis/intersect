# import httpx
# import time
# import asyncio
# import pandas as pd
# from selectolax.lexbor import LexborHTMLParser
# from extract import scrape

# INPUT_FILEPATH = "intersect/data/facilitator.feather"


# async def get_description(url: str) -> str | None:
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await scrape(client, url)
#             print(f"OK: {url}")
#     except Exception as e:
#         print(f"Failed to scrape {url}: {e}")
#         return None

#     parser = LexborHTMLParser(response.text)
#     result = parser.css_first(".job__description")

#     if result is None:
#         return None

#     return result.text().strip()


# async def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:
#     semaphore = asyncio.Semaphore(10)

#     async with semaphore:
#         tasks = [get_description(url) for url in df["url"]]
#         descriptions = await asyncio.gather(*tasks)

#     df["description"] = descriptions
#     return df


# async def main():
#     start_time = time.time()

#     df = pd.read_feather(INPUT_FILEPATH)
#     df = await get_descriptions(df)
#     df.to_feather(INPUT_FILEPATH)

#     end_time = time.time()
#     print(f"Execution time: {end_time - start_time} seconds")


# if __name__ == "__main__":
#     asyncio.run(main())

import httpx
import time
import asyncio
import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape

INPUT_FILEPATH = "intersect/data/facilitator.feather"
SEMAPHORE_LIMIT = 10


async def get_description(client: httpx.AsyncClient, url: str, index: int, semaphore: asyncio.Semaphore) -> tuple[int, str | None]:
    """
    Fetch the job description from the given URL.
    """
    async with semaphore:
        try:
            response = await scrape(client, url)
            print(f"OK: {url}")
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return index, None

        parser = LexborHTMLParser(response.text)
        result = parser.css_first(".job__description")

        if result is None:
            return index, None

        return index, result.text().strip()


async def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fetch job descriptions for all URLs in the DataFrame.
    Process tasks as they are completed but maintain the original order in the DataFrame.
    """
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async with httpx.AsyncClient() as client:
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

    # Assign descriptions back to the DataFrame
    descriptions = [desc for _, desc in results]
    df["description"] = descriptions

    return df


async def main():
    """
    Main function to read the DataFrame, fetch descriptions, and save the result.
    """
    start_time = time.time()

    try:
        df = pd.read_feather(INPUT_FILEPATH)
        print(f"Loaded {len(df)} URLs from {INPUT_FILEPATH}")

        df = await get_descriptions(df)
        print(f"Scraped descriptions for {len(df)} rows.")

        df.to_feather(INPUT_FILEPATH)
        print(f"Updated DataFrame saved to {INPUT_FILEPATH}")
    except Exception as e:
        print(f"Error occurred during scraping: {e}")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
