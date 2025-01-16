import pandas as pd
from scrape_descriptions import get_descriptions
import time

INPUT_FILEPATH = "intersect/data/leadership.feather"


def main():
    start_time = time.time()

    df = pd.read_feather(INPUT_FILEPATH)
    df = get_descriptions(df)
    df.to_feather(INPUT_FILEPATH)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
