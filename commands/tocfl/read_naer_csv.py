# source: https://coct2.naer.edu.tw/download/tech_report/

import pandas as pd
from pathlib import Path

"""
Columns explanation: 
The + means to keep the field, - means to discard the field.

+ 序號: id (used as pandas index)
+ 詞語: word in Mandarin
- 級別: level/difficulty (could be useful in the future)
+ 注音: zhuyin (shown alongside the word)
+ 漢拼: pinyin (shown alongside the word)
- 詞類/性質: word category/nature (e.g., noun, verb, adjective)
+ 詞彙英譯: English translation (quiz choice)
- 語義/義項: usually empty, so unused
- 情境: context
- 用法-常用搭配詞: usage-common collocations
- 例句: example sentence (not always present)
"""

INDEX_COL = 0
# to save memory, only keep the columns we need
COLS_TO_KEEP = ("詞語", "注音", "漢拼", "詞彙英譯", "詞類/性質")
WORD_TYPES_TO_REMOVE = ("Ptc", "Prep") # Particles (like 的), Prepositions (like 在)

def read_naer_csv_raw(
    filepath: Path,
    index_col: int = INDEX_COL,
    cols_to_keep: tuple = COLS_TO_KEEP,
) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding='utf-8', index_col=index_col)
    if cols_to_keep:
        df = df[list(cols_to_keep)]
    df = df.fillna("")  # replace all NaN with empty string
    # drop all rows where 詞語 is empty
    df = df[df["詞語"] != ""]
    # remove word types we don't want
    df = df[~df["詞類/性質"].isin(WORD_TYPES_TO_REMOVE)]
    # rename columns to english
    df.rename(columns={"詞語": "word", "注音": "zhuyin", "漢拼": "pinyin", "詞彙英譯": "english"}, inplace=True)
    return df.drop(columns=["詞類/性質"])

NAER_PATH = Path(__file__).parent / "naer.csv" # not actually tocfl
NAER_CSV = read_naer_csv_raw(NAER_PATH)

# if __name__ == "__main__":
#     print(NAER_CSV.sample(5))