import pandas as pd
import numpy as np
from selectolax.lexbor import LexborHTMLParser

OUTPUT_PATH = "intersect/data/jobs2.feather"


def load(data: list, path: str):
    df = pd.DataFrame(data)
    df.to_feather(path)


def transform_cvlibrary(html: str):
    parser = LexborHTMLParser(html)
    results = parser.css("li.results__item")
    return [transform_item_cvlibrary(x) for x in results]


def transform_item_cvlibrary(result):
    article = result.css_first("article.job")

    return {
        "title": article.attributes.get("data-job-title"),
        "company": article.attributes.get("data-company-name"),
        "location": article.attributes.get("data-job-location"),
        "salary": article.attributes.get("data-job-salary"),
        "type": article.attributes.get("data-job-type"),
        "posted": article.attributes.get("data-job-posted"),
        "job_industry": article.attributes.get("data-job-industry"),
        # abstract
        # full description
        # url
    }


def main():
    with open("intersect/data/raw/jobs.txt", "r") as f:
        html = f.read()

    data = transform_cvlibrary(html)
    load(data, OUTPUT_PATH)


if __name__ == "__main__":
    main()
