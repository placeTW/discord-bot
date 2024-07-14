import pandas as pd
from pathlib import Path

# source: https://github.com/ChhoeTaigi/ChhoeTaigiDatabase?tab=readme-ov-file

"""
Embree's file format (using the example of 'ut-táu' for most of the fields).
The + means to keep the field, - means to discard the field.

+ DictWordID: '番號', (unique id, used as index in this script)
+ PojUnicode: '白話字', (Taiwanese Romanization, e.g., 'ut-táu')
+ PojInput: '白話字輸入', (Taiwanese Romanization input, e.g., 'ut-tau2')
- KipUnicode: '教育部羅馬拼音', (Ministry of Education Romanization, e.g., 'ut-táu')
- KipInput: '教育部羅馬拼音輸入', (Ministry of Education Romanization input, e.g., 'ut-tau2')
+ Abbreviation: '詞類縮寫', (Word class abbreviation, e.g., 'N' for noun)
+ NounClassifier: '單位量詞', (Unit classifier, e.g., 'ê' for mandarin '個')
- Reduplication: '疊詞', (Reduplication, e.g., 'hóng-hóng-hut-hut' for 'hóng-hut' (mandarin for '恍惚'))
+ HoaBun: '對應華文', (Mandarin equivalent, e.g., '熨斗')
+ EngBun: '對應英文', (English equivalent, e.g., 'iron (for clothes)')
- Synonym: 'Kāng義詞', (Synonym, e.g., 'hóng-hut')
- Confer: '參照', (Reference to another entry, probably PojUnicode field)
- PageNumber: '原冊頁數', (Page number in the original dictionary, e.g., '123') 
"""

INDEX_COL = 0
# to save memory, only keep the columns we need
COLS_TO_KEEP = ("PojUnicode", "PojInput", "Abbreviation", "NounClassifier", "HoaBun", "EngBun")

def read_embree_csv_raw(
    filepath: Path,
    index_col: int = INDEX_COL,
    cols_to_keep: tuple = COLS_TO_KEEP,
) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding='utf-8', index_col=index_col)
    if cols_to_keep:
        df = df[list(cols_to_keep)]
    return df

def get_random_row(df: pd.DataFrame) -> pd.Series:
    return df.sample().iloc[0]