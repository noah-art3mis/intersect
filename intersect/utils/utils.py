import pandas as pd
import logging
import numpy as np

def add_you(df: pd.DataFrame, input_text: str, vector: list[float]) -> pd.DataFrame:

    new_row_index = len(df)
    df.loc[new_row_index, "title"] = "Your text"
    df.loc[new_row_index, "description"] = input_text
    df.at[new_row_index, "embedding"] = vector
    return df


def add_index(df: pd.DataFrame, column: str, new_index: str) -> pd.DataFrame:
    df.sort_values(by=column, ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df[new_index] = df.index
    return df


def format_salary(row: pd.Series, currency: str = "£") -> str:
    """Format salary information for display"""
    min_salary = row['minimum_salary']
    max_salary = row['maximum_salary']
    
    if min_salary is "" or max_salary is "":
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    if min_salary is None or max_salary is None:
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    if min_salary is np.nan or max_salary is np.nan:
        logging.warning(f"Salary information is missing for job {row['job_id']}")
        return ""

    return f"{currency}{min_salary:,} - {currency}{max_salary:,}"