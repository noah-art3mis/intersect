import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape_search
import httpx

def get_description(url: str) -> str | None:
    try:
        with httpx.Client() as client:
            response = scrape_search(client, url)
            print(f"OK: {url}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

    parser = LexborHTMLParser(response.text)
    result = parser.css_first(".job__description")

    if result is None:
        return None

    return result.text().strip()


def get_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    df["description"] = df["url"].apply(get_description)
    return df
