import os
import pandas as pd
import numpy as np
from selectolax.lexbor import LexborHTMLParser
from selectolax.lexbor import LexborNode
from urllib.parse import urljoin

OUTPUT_PATH = "intersect/data/jobs2.feather"


def load(data: list, path: str) -> None:
    df = pd.DataFrame(data)
    df.to_feather(path)


def get_url(article: LexborNode) -> str | None:
    BASE_URL = "https://www.cv-library.co.uk/"

    element = article.css_first(".job__description-more")

    if element is None:
        return None

    path = element.attributes.get("href")

    if path is None:
        return None

    return urljoin(BASE_URL, path)


def not_ad(item: LexborNode) -> bool:
    """Some elements are ads and can be filtered out by observing their lack of data."""
    element = item.css_first("article.job").css_first(".job__description-more")
    return True if element is not None else False


def transform_cvlibrary(html: str) -> list:
    parser = LexborHTMLParser(html)
    results = parser.css("li.results__item")
    return [transform_item_cvlibrary(x) for x in results if not_ad(x)]


def transform_item_cvlibrary(item: LexborNode) -> dict:

    article = item.css_first("article.job")

    return {
        "title": article.attributes.get("data-job-title"),
        "company": article.attributes.get("data-company-name"),
        "location": article.attributes.get("data-job-location"),
        "salary": article.attributes.get("data-job-salary"),
        "type": article.attributes.get("data-job-type"),
        "posted": article.attributes.get("data-job-posted"),
        "job_industry": article.attributes.get("data-job-industry"),
        "abstract": article.css_first(".job__description").text().strip(),
        "url": get_url(article),
    }


def main():
    with open("intersect/data/raw/jobs.txt", "r") as f:
        html = f.read()

    data = transform_cvlibrary(html)
    load(data, OUTPUT_PATH)


if __name__ == "__main__":
    main()
