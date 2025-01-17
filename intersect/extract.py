import asyncio
import uuid
import os
import time
import httpx
from dotenv import load_dotenv

# https://www.cv-library.co.uk/ai-jobs-in-london?page=1&perpage=100&us=1
# https://www.cv-library.co.uk/ai-jobs-in-london?page=2&perpage=100&us=1

KEYWORDS = "innovation"
LOCATION = "london"
N_PAGES = 5
PERPAGE = 100


def setup_url(keywords: str, location: str, page: int, perpage: int):
    """pls be nice to this function and use simple search terms. dont stress test this."""
    # what happens to cities with spaces in the name?
    # what happens to keywords with special characters
    # what if last character is also a -?
    # fix this using unidecode

    return f"https://www.cv-library.co.uk/{keywords.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}?page={page}&perpage={perpage}&us=1"


async def scrape_search(client: httpx.AsyncClient, url: str) -> httpx.Response:
    response = await client.get(
        url="https://proxy.scrapeops.io/v1/",
        params={
            "api_key": os.environ["SCRAPEOPS_API_KEY"],
            "url": url,
        },
        timeout=100,
        # follow_redirects=True,
    )
    return response


async def scrape_all_pages(
    client: httpx.AsyncClient, keywords: str, location: str, n_pages: int, perpage: int
):
    for page in range(1, n_pages + 1):
        url = setup_url(keywords, location, page, perpage=perpage)
        response = await scrape_search(client, url)
        response.raise_for_status()
        print(f"{response.status_code}: Scraped {url}")
        yield response


async def main():
    load_dotenv()
    async with httpx.AsyncClient() as client:
        async for response in scrape_all_pages(
            client, KEYWORDS, LOCATION, N_PAGES, PERPAGE
        ):
            with open(f"jobs-{uuid.uuid4()}.txt", "w") as f:
                f.write(response.text)
                time.sleep(1)
    print("done")


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


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
