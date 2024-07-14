import pandas as pd
from pathlib import Path

def get_random_row(df: pd.DataFrame) -> pd.Series:
    return df.sample().iloc[0]