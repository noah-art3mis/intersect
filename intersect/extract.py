import asyncio
import os
import time
import httpx
from dotenv import load_dotenv

# https://www.cv-library.co.uk/ai-jobs-in-london?page=1&perpage=100&us=1
# https://www.cv-library.co.uk/ai-jobs-in-london?page=2&perpage=100&us=1

KEYWORDS = "data"
LOCATION = "london"
N_PAGES = 5
PERPAGE = 100
SEMAPHORE = 5


def setup_url(keywords: str, location: str, page: int, perpage: int):
    """pls be nice to this function and use simple search terms. dont stress test this."""
    # what happens to cities with spaces in the name?
    # what happens to keywords with special characters
    # what if last character is also a -?
    # fix this using unidecode

    return f"https://www.cv-library.co.uk/{keywords.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}?page={page}&perpage={perpage}&us=1"


async def scrape_page(
    client: httpx.AsyncClient, url: str, index: int, semaphore: asyncio.Semaphore
):
    result = await scrape(client, url, semaphore)
    return (index, result)


async def scrape(
    client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore
) -> httpx.Response:
    async with semaphore:
        try:
            start_time = time.time()
            response = await client.get(
                url="https://proxy.scrapeops.io/v1/",
                params={
                    "api_key": os.environ["SCRAPEOPS_API_KEY"],
                    "url": url,
                },
                timeout=100,
            )
            response.raise_for_status()
            end_time = time.time()
            print(
                f"{response.status_code} : {end_time - start_time:.2f}s : Scraped {url}"
            )
            return response
        except Exception as e:
            print("!!! Failed to scrape", url, e)
            return httpx.Response(status_code=500)


async def scrape_all_pages(keywords: str, location: str, n_pages: int, perpage: int):
    semaphore = asyncio.Semaphore(SEMAPHORE)
    
    async with httpx.AsyncClient() as client:

        urls = [
            setup_url(keywords, location, page, perpage=perpage)
            for page in range(1, n_pages + 1)
        ]

        tasks = [
            scrape_page(client, url, index, semaphore) for index, url in enumerate(urls)
        ]

        return await asyncio.gather(*tasks)


def extract_jobs(keywords: str, location: str, n_pages: int, perpage: int):
    responses = asyncio.run(scrape_all_pages(keywords, location, n_pages, perpage))
    responses.sort(key=lambda x: x[0])

    for index, response in responses:
        OUTPATH = f"intersect/data/raw/{KEYWORDS}"

        if not os.path.exists(OUTPATH):
            os.makedirs(OUTPATH)

        filepath = f"{index}-{KEYWORDS.replace(' ', '-')}.txt"

        with open(os.path.join(OUTPATH, filepath), "w") as f:
            f.write(response.text)


def main():
    load_dotenv()
    start_time = time.time()
    extract_jobs(KEYWORDS, LOCATION, N_PAGES, PERPAGE)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()


# alternatives
# url = 'https://books.toscrape.com/'
# url = "https://www.cv-library.co.uk/ai-jobs-in-london?perpage=25&us=1"
# url = "https://uk.indeed.com/jobs?q=ai&l=london&from=searchOnHP&vjk=ca59d58f6db9887c"

# scrapeops or zenrows or bright or proxyscrape
# https://scrapeops.io/web-scraping-playbook/
# https://scrapeops.io/web-scraping-playbook/how-to-scrape-indeed/
# https://www.zenrows.com/blog/web-scraping-headers#upgrade-insecure-request
# https://scrapeops.io/web-scraping-playbook/web-scraping-guide-header-user-agents/
# https://scrapeops.io/docs/fake-user-agent-headers-api/fake-browser-headers/

# def request_with_fake_headers():
#     fake_headers = httpx.get(
#         url="https://headers.scrapeops.io/v1/browser-headers",
#         params={"api_key": os.environ["SCRAPEOPS_API_KEY"], "num_results": "1"},
#     )

#     res = httpx.get(
#         url="https://www.cv-library.co.uk/ai-jobs-in-london?perpage=25&us=1",
#         headers=fake_headers.json()["result"][0],
#     )

#     print(res)
