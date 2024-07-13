import pytest
from functions.reacts import evaluate_event_condition

@pytest.fixture
def match_link_ids():
    return {'baltic_meows', 'tw', 'hgs'}

def test_single_true_condition(match_link_ids):
    assert evaluate_event_condition("baltic_meows", match_link_ids) == True

def test_single_false_condition(match_link_ids):
    assert evaluate_event_condition("non_existent", match_link_ids) == False

def test_or_condition_true(match_link_ids):
    assert evaluate_event_condition("baltic_meows or non_existent", match_link_ids) == True

def test_or_condition_false(match_link_ids):
    assert evaluate_event_condition("non_existent1 or non_existent2", match_link_ids) == False

def test_and_condition_true(match_link_ids):
    assert evaluate_event_condition("baltic_meows and tw", match_link_ids) == True

def test_and_condition_false(match_link_ids):
    assert evaluate_event_condition("baltic_meows and non_existent", match_link_ids) == False

def test_not_condition_true(match_link_ids):
    assert evaluate_event_condition("not non_existent", match_link_ids) == True

def test_not_condition_false(match_link_ids):
    assert evaluate_event_condition("not baltic_meows", match_link_ids) == False

def test_complex_condition_true(match_link_ids):
    assert evaluate_event_condition("(baltic_meows or non_existent) and (tw or hgs)", match_link_ids) == True

def test_complex_condition_false(match_link_ids):
    assert evaluate_event_condition("(baltic_meows and non_existent) or (not tw and not hgs)", match_link_ids) == False

def test_all_link_ids(match_link_ids):
    assert evaluate_event_condition("baltic_meows and tw and hgs", match_link_ids) == True

def test_empty_match_link_ids():
    assert evaluate_event_condition("baltic_meows", set()) == False

def test_no_match_link_ids():
    assert evaluate_event_condition("baltic_meows", None) == True

def test_empty_condition(match_link_ids):
    with pytest.raises(SyntaxError):
        evaluate_event_condition("", match_link_ids)

def test_invalid_syntax(match_link_ids):
    with pytest.raises(SyntaxError):
        evaluate_event_condition("baltic_meows and and tw", match_link_ids)
