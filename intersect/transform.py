import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from selectolax.lexbor import LexborNode
from urllib.parse import urljoin
import os

INPUT_PATH = "intersect/data/raw/law"
OUTPUT_PATH = "intersect/data/law.feather"


def cvlibrary_text2feather(input_path: str, output_path: str) -> None:
    for file in sorted(os.listdir(input_path)):
        with open(os.path.join(input_path, file), "r") as f:
            html = f.read()
            data = transform_cvlibrary(html)
            load(data, output_path)


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


def load(data: list, path: str) -> None:
    new_df = pd.DataFrame(data)

    if os.path.exists(path):
        existing_df = pd.read_feather(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.drop_duplicates(subset=None, keep="first", inplace=False)

    combined_df.to_feather(path)

    print(f"Saved to {path}")
    print(f"n_rows: {combined_df.shape[0]}")


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


def main():
    cvlibrary_text2feather(INPUT_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()
