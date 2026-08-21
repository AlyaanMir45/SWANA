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


# Test the average operation
def test_average_request():
    result = interpret_request(
        "What is the average annual salary?"
    )

    assert result["operation"] == "average"
    assert result["column"] == "annual_salary"


# Test the sum operation
def test_sum_request():
    result = interpret_request(
        "What is the sum of annual salary?"
    )

    assert result["operation"] == "sum"
    assert result["column"] == "annual_salary"


# Test the count operation
def test_count_request():
    result = interpret_request(
        "Count the rows"
    )

    assert result["operation"] == "count"