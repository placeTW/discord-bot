# source: https://coct2.naer.edu.tw/download/tech_report/

import pandas as pd
from pathlib import Path

"""
Columns explanation: 
The + means to keep the field, - means to discard the field.

+ en: English word
+ md: Mandarin word (used as choices in quiz)

The index is the default pandas index.
"""

def read_naer_MD_csv_raw(
    filepath: Path,
) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding='utf-8', index_col=None)
    df = df.fillna("")  # replace all NaN with empty string
    df = df.dropna() # drop all rows where en or md is empty
    return df

NAER_MD_PATH = Path(__file__).parent / "naer_MD.csv" # not actually tocfl
NAER_MD_CSV = read_naer_MD_csv_raw(NAER_MD_PATH)

if __name__ == "__main__":
    print(NAER_MD_CSV.sample(5))
    print(len(NAER_MD_CSV))
    print(len(NAER_MD_CSV.drop_duplicates(subset=["en"])))  # check for duplicates