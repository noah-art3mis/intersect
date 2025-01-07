import pandas as pd
from selectolax.lexbor import LexborHTMLParser
from extract import scrape_search

DB_URL = "./intersect/data/jobs2.feather"
df = pd.read_feather(DB_URL)


def get_description(url: str) -> str:
    html = scrape_search(url)
    parser = LexborHTMLParser(html)
    return parser.css_first(".job__description").text().strip()


df["description"] = df["url"].apply(get_description)

df.to_feather(DB_URL)