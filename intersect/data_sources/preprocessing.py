from datetime import datetime
import pandas as pd
import re
import html

from utils.utils import format_salary


def preprocess_jobs(df: pd.DataFrame) -> pd.DataFrame:
    df = calculate_salary(df)
    df = clean_web_artifacts(df)
    # df = calculate_days_ago(df) # reef doesnt have a posted date
    return df

def clean_web_artifacts(df: pd.DataFrame) -> pd.DataFrame:
    df['description'] = (df['description']
            .astype(str)
            .str.replace(r'\n', ' ')
            .apply(html.unescape)
            .str.replace(r'<[^>]+>', '', regex=True) 
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )
    return df

def calculate_salary(df: pd.DataFrame) -> pd.DataFrame:
    df['salary'] = df.apply(format_salary, axis=1)
    return df

def calculate_days_ago(df: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now(tz=pd.Timestamp.utcnow().tz)
    df['days_ago'] = (now - pd.to_datetime(df["posted"], utc=True)).dt.days
    return df