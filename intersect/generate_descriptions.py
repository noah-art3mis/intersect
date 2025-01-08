import pandas as pd
from scrape_descriptions import get_descriptions

INPUT_FILEPATH = "intersect/data/jobs-144.feather"

df = pd.read_feather(INPUT_FILEPATH)
df = get_descriptions(df)
df.to_feather(INPUT_FILEPATH)
