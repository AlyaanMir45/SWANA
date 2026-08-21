import pandas as pd
import pytest

from src.dispatcher import dispatch_command


# Test the average operation
def test_average():
    dataframe = pd.DataFrame({
        "age": [20, 30, 40]
    })

    command = {
        "operation": "average",
        "column": "age"
    }

    result = dispatch_command(dataframe, command)

    # Check that the average is correct
    assert result == 30


# Test the count operation
def test_count():
    dataframe = pd.DataFrame({
        "name": ["John", "Sara", "Mike"]
    })

    command = {
        "operation": "count"
    }

    result = dispatch_command(dataframe, command)

    # Check that all rows are counted
    assert result == 3


# Test removing duplicate rows
def test_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["John", "John", "Sara"]
    })

    command = {
        "action": "remove_duplicates",
        "parameters": {}
    }

    result = dispatch_command(dataframe, command)

    # Check that the duplicate row was removed
    assert len(result) == 2


# Test removing rows with missing values
def test_remove_missing_rows():
    dataframe = pd.DataFrame({
        "age": [20, None, 40]
    })

    command = {
        "action": "remove_missing_rows",
        "parameters": {}
    }

    result = dispatch_command(dataframe, command)

    # Check that the missing row was removed
    assert len(result) == 2


# Test filling missing values
def test_fill_missing_values():
    dataframe = pd.DataFrame({
        "age": [20, None, 40]
    })

    command = {
        "action": "fill_missing_values",
        "parameters": {
            "value": 0
        }
    }

    result = dispatch_command(dataframe, command)

    # Check that there are no missing values
    assert result["age"].isna().sum() == 0


# Test an invalid command
def test_invalid_command():
    dataframe = pd.DataFrame({
        "age": [20, 30]
    })

    command = {
        "action": "invalid"
    }

    # Check that an invalid command causes an error
    with pytest.raises(ValueError):
        dispatch_command(dataframe, command)