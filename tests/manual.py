from curl_cffi import requests
from urllib.parse import urlencode
from rich import print

KEYWORDS = "law"
LOCATION = "london"
N_PAGES = 2
PERPAGE = 100
SEMAPHORE = 3

def setup_url(keywords: str, location: str, page: int, perpage: int) -> str:
    base_url = "https://www.cv-library.co.uk/"

    query_params = {
        "page": page,
        "perpage": perpage,
        "us": 1
    }

    query_string = urlencode(query_params)
    keywords_encoded = keywords.replace(' ', '-')
    location_encoded = location.replace(' ', '-')

    return f"{base_url}{keywords_encoded}-jobs-in-{location_encoded}?{query_string}"


URL = setup_url(KEYWORDS, LOCATION, N_PAGES, PERPAGE)
r = requests.get(URL, impersonate="chrome")
print(r.text)