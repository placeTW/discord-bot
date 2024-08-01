import pytest
from commands.taiwanese.read_embree_csv import TW_EMBREE_CSV, NUM_WORDS_COL, _count_taigi_words

def test_num_words_col():
    """Test the integrity of the column."""
    # assert that the column exists
    assert NUM_WORDS_COL in TW_EMBREE_CSV.columns
    # assert it contains only integers
    assert TW_EMBREE_CSV[NUM_WORDS_COL].dtype == int
    # assert that there are no negative values
    assert (TW_EMBREE_CSV[NUM_WORDS_COL] >= 0).all()

@pytest.mark.parametrize(
    "poj,expected", 
    [
        ("", 0),
        ("thǹg", 1),
        ("thǹg-bō", 2),
        ("thǹg-chhiah-kha", 3),
        ("thn̂g-chhò͘-pâi-kut", 4),
        ("àm-hông-lián-ong-eng", 5),
        ("Tâi-oân-tài-bùn-siông-chhú", 6),
        ("lêng-géng-bo̍k-ia̍p-kài-khak-thâng", 7),
    ])
def test__count_taigi_words(poj: str, expected: str):
    """Test the _count_taigi_words function."""
    assert _count_taigi_words(poj) == expected

# these are problematic cases, but we write the cases first but skip them
@pytest.mark.skip(reason="These cases are problematic")
@pytest.mark.parametrize(
    "poj,expected", 
    [
        ("tû-khì + N + í-gōa", 4),
        ("tû-liáu + N + í-gōa", 4),
    ]
)
def test__count_taigi_words_problematic(poj: str, expected: str):
    """Test the _count_taigi_words function."""
    assert _count_taigi_words(poj) == expected