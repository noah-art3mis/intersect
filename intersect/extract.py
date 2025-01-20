import asyncio
import os
import time
from curl_cffi.requests import AsyncSession, Response
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from dotenv import load_dotenv
from urllib.parse import urlencode
from transform import cvlibrary_text2feather
import random
from rich import print

# Configuration
KEYWORDS = "data"
LOCATION = "london"
N_PAGES = 5
PERPAGE = 100
SEMAPHORE = 3


async def scrape_all_pages(keywords: str, location: str, n_pages: int, perpage: int):

    semaphore = asyncio.Semaphore(SEMAPHORE)

    async with AsyncSession() as client:
        urls = [
            setup_url_cvlibrary(keywords, location, page, perpage=perpage)
            for page in range(1, n_pages + 1)
        ]

        tasks = [scrape(client, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        indexed_results = [
            (i, result) for i, result in enumerate(results) if result is not None
        ]
        return indexed_results


@retry(
    stop=stop_after_attempt(3),  # Retry up to 3 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff
    reraise=True,  # Raise the exception if all retries fail
)
async def fetch_with_retry(client: AsyncSession, url: str, proxy: str) -> Response:
    start_time = time.time()
    response = await client.get(
        url,
        impersonate="chrome",
        proxies={
            "http": f"http://{proxy}",
        },
    )
    end_time = time.time()
    print(
        f"{response.status_code if response else 'Failed'} : {end_time - start_time:.2f}s : Scraped {url[:50] + '...' if len(url) > 50 else url}"
    )
    return response


async def scrape(
    client: AsyncSession, url: str, semaphore: asyncio.Semaphore
) -> Response | None:
    proxies = get_proxies("proxies.txt")
    proxy = random.choice(proxies)

    async with semaphore:
        try:
            return await fetch_with_retry(client, url, proxy)
        except RetryError as e:
            print(f"Failed to scrape {url} after multiple attempts - {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while scraping {url} - {e}")
            return None


def get_proxies(path):
    proxies = []
    with open(path, "r") as f:
        for line in f:
            proxies.append(line.strip())
    return proxies


def setup_url_cvlibrary(keywords: str, location: str, page: int, perpage: int) -> str:
    base_url = "https://www.cv-library.co.uk/"

    query_params = {"page": page, "perpage": perpage, "us": 1}

    query_string = urlencode(query_params)
    keywords_encoded = keywords.replace(" ", "-")
    location_encoded = location.replace(" ", "-")

    return f"{base_url}{keywords_encoded}-jobs-in-{location_encoded}?{query_string}"


def save_jobs(responses: list, keywords: str):
    """Save job responses to disk, as txt and as feather."""

    OUTPATH_TXT = f"intersect/data/raw/{keywords.replace(' ', '-')}"
    os.makedirs(OUTPATH_TXT, exist_ok=True)

    OUTPATH_FEATHER = f"intersect/data/{keywords.replace(' ', '-')}.feather"

    for index, response in responses:
        filename = f"{index}-{keywords.replace(' ', '-')}.txt"
        filepath = os.path.join(OUTPATH_TXT, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response)

    cvlibrary_text2feather(
        input_path=OUTPATH_TXT,
        output_path=OUTPATH_FEATHER,
    )


def main():
    start_time = time.time()

    load_dotenv()
    responses = asyncio.run(scrape_all_pages(KEYWORDS, LOCATION, N_PAGES, PERPAGE))
    responses_text = [(index, response.text) for index, response in responses]
    save_jobs(responses_text, KEYWORDS)

    end_time = time.time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
