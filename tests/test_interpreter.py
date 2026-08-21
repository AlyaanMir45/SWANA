import pytest

from src.interpreter import interpret_request


# Test removing duplicate rows
def test_remove_duplicates():
    result = interpret_request("Remove duplicate rows")

    assert result["action"] == "remove_duplicates"
    assert result["parameters"] == {}


# Test another duplicate phrase
def test_duplicates_phrase():
    result = interpret_request("Delete all duplicates")

    assert result["action"] == "remove_duplicates"


# Test removing missing rows
def test_remove_missing_rows():
    result = interpret_request("Remove rows with missing values")

    assert result["action"] == "remove_missing_rows"


# Test removing empty columns
def test_remove_empty_columns():
    result = interpret_request("Delete blank columns")

    assert result["action"] == "remove_empty_columns"


# Test standardizing column names
def test_standardize_column_names():
    result = interpret_request("Standardize column names")

    assert result["action"] == "standardize_column_names"


# Test an unknown request
def test_unknown_request():
    with pytest.raises(ValueError):
        interpret_request("Make the dataset better")