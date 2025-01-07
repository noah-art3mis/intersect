import os
import httpx
from dotenv import load_dotenv

URL = "https://www.cv-library.co.uk/ai-jobs-in-london?perpage=25&us=1"
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


def scrape_search(url: str) -> str:
    load_dotenv()
    response = httpx.get(
        url="https://proxy.scrapeops.io/v1/",
        params={
            "api_key": os.environ["SCRAPEOPS_API_KEY"],
            "url": url,
        },
        timeout=100,
    )
    return response.text


def main():
    html = scrape_search(URL)

    with open("jobs.txt", "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
