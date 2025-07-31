import pandas as pd


def add_you(df: pd.DataFrame, input_text: str, vector: list[float]) -> pd.DataFrame:

    new_row_index = len(df)
    df.loc[new_row_index, "title"] = "Your text"
    df.loc[new_row_index, "description"] = input_text
    df.at[new_row_index, "embedding"] = vector
    return df


def add_index(df: pd.DataFrame, column: str, new_index: str) -> pd.DataFrame:
    df = df.sort_values(by=column, ascending=False)
    df = df.reset_index(drop=True)
    df[new_index] = df.index
    return df
