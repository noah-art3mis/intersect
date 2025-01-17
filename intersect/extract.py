import asyncio
import os
import time
import httpx
from dotenv import load_dotenv
from transform import cvlibrary_text2feather

# Configuration
KEYWORDS = "law"
LOCATION = "london"
N_PAGES = 2
PERPAGE = 100
SEMAPHORE = 3


async def scrape_all_pages(keywords: str, location: str, n_pages: int, perpage: int):
    """Scrape all pages with concurrency control."""
    semaphore = asyncio.Semaphore(SEMAPHORE)
    async with httpx.AsyncClient() as client:
        urls = [
            setup_url(keywords, location, page, perpage=perpage)
            for page in range(1, n_pages + 1)
        ]

        tasks = [scrape(client, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        # Attach the index for sorting later
        indexed_results = [
            (i, result) for i, result in enumerate(results) if result is not None
        ]
        return indexed_results


async def scrape(
    client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore
) -> httpx.Response | None:
    """Scrape a single page with concurrency control."""
    async with semaphore:
        try:
            start_time = time.time()
            response = await client.get(
                url="https://proxy.scrapeops.io/v1/",
                params={
                    "api_key": os.environ["SCRAPEOPS_API_KEY"],
                    "url": url,
                },
                timeout=50,
            )
            response.raise_for_status()
            end_time = time.time()
            print(
                f"{response.status_code} : {end_time - start_time:.2f}s : Scraped {url}"
            )
            return response
        except Exception as e:
            print(f"!!! Failed to scrape {url} - {e}")
            return None


def setup_url(keywords: str, location: str, page: int, perpage: int):
    """Generate the target URL."""
    return f"https://www.cv-library.co.uk/{keywords.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}?page={page}&perpage={perpage}&us=1"


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
