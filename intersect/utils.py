import pandas as pd


def add_you(prev_df: pd.DataFrame, input_text: str, vector: list[float]) -> pd.DataFrame:
    your_text = pd.Series(
        {
            "Rank": None,
            "Title": "Your text",
            "Delta": None,
            "Similarity": None,
            "Description": input_text,
            "Link": None,
            "Vector": vector,
            "Cluster": "You",
        }
    )
    df = pd.concat([prev_df, your_text], ignore_index=True)
    return df