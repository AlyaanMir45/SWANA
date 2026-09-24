
import pandas as pd
import pytest

from src.dispatcher import dispatch_command


# Create a sample dataset for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "department": ["IT", "IT", "Finance", "Finance"],
        "annual_salary": [60000, 80000, 70000, 90000],
    })


# Test removing duplicate rows
def test_dispatch_remove_duplicates():
    dataframe = pd.DataFrame({
        "department": ["IT", "IT", "Finance"],
        "annual_salary": [60000, 60000, 90000],
    })

    command = {
        "action": "remove_duplicates",
        "parameters": {},
    }

    result = dispatch_command(dataframe, command)

    assert len(result) == 2


# Test removing rows with missing values
def test_dispatch_remove_missing_rows():
    dataframe = pd.DataFrame({
        "department": ["IT", None, "Finance"],
        "annual_salary": [60000, 80000, 90000],
    })

    command = {
        "action": "remove_missing_rows",
        "parameters": {},
    }

    result = dispatch_command(dataframe, command)

    assert len(result) == 2


# Test removing completely empty columns
def test_dispatch_remove_empty_columns():
    dataframe = pd.DataFrame({
        "department": ["IT", "Finance"],
        "empty_column": [None, None],
    })

    command = {
        "action": "remove_empty_columns",
        "parameters": {},
    }

    result = dispatch_command(dataframe, command)

    assert "empty_column" not in result.columns


# Test standardizing column names
def test_dispatch_standardize_column_names():
    dataframe = pd.DataFrame({
        "Annual Salary": [60000, 80000],
    })

    command = {
        "action": "standardize_column_names",
        "parameters": {},
    }

    result = dispatch_command(dataframe, command)

    assert "annual_salary" in result.columns


# Test calculating the average
def test_dispatch_average(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    assert result == 75000


# Test calculating the sum
def test_dispatch_sum(sample_dataframe):
    command = {
        "operation": "sum",
        "column": "annual_salary",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    assert result == 300000


# Test calculating the minimum
def test_dispatch_minimum(sample_dataframe):
    command = {
        "operation": "minimum",
        "column": "annual_salary",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    assert result == 60000


# Test calculating the maximum
def test_dispatch_maximum(sample_dataframe):
    command = {
        "operation": "maximum",
        "column": "annual_salary",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    assert result == 90000


# Test calculating the median
def test_dispatch_median(sample_dataframe):
    command = {
        "operation": "median",
        "column": "annual_salary",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    assert result == 75000


# Test grouped average
def test_dispatch_grouped_average(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "department",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    it_average = result.loc[
        result["department"] == "IT",
        "average",
    ].iloc[0]

    finance_average = result.loc[
        result["department"] == "Finance",
        "average",
    ].iloc[0]

    assert it_average == 70000
    assert finance_average == 80000


# Test grouped sum
def test_dispatch_grouped_sum(sample_dataframe):
    command = {
        "operation": "sum",
        "column": "annual_salary",
        "group_by": "department",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    it_sum = result.loc[
        result["department"] == "IT",
        "sum",
    ].iloc[0]

    assert it_sum == 140000


# Test grouped count
def test_dispatch_grouped_count(sample_dataframe):
    command = {
        "operation": "count",
        "group_by": "department",
    }

    result = dispatch_command(
        sample_dataframe,
        command,
    )

    it_count = result.loc[
        result["department"] == "IT",
        "count",
    ].iloc[0]

    finance_count = result.loc[
        result["department"] == "Finance",
        "count",
    ].iloc[0]

    assert it_count == 2
    assert finance_count == 2


# Test calculating the average salary for IT
def test_filtered_average(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "IT",
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 70000


# Test calculating the total salary for Finance
def test_filtered_sum(sample_dataframe):
    command = {
        "operation": "sum",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "Finance",
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 160000


# Test counting employees in IT
def test_filtered_count(sample_dataframe):
    command = {
        "operation": "count",
        "filter": {
            "column": "department",
            "value": "IT",
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 2


# Test filtering with a column that does not exist
def test_invalid_filter_column(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "invalid_column",
            "value": "IT",
        },
    }

    with pytest.raises(ValueError, match="Filter column"):
        dispatch_command(sample_dataframe, command)


# Test filtering when no rows match
def test_filter_no_matches(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "Marketing",
        },
    }

    with pytest.raises(ValueError, match="No rows found"):
        dispatch_command(sample_dataframe, command)


# Test that filtering does not modify the original dataset
def test_filter_preserves_dataset(sample_dataframe):
    original = sample_dataframe.copy(deep=True)

    command = {
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "IT",
        },
    }

    dispatch_command(sample_dataframe, command)

    pd.testing.assert_frame_equal(
        sample_dataframe,
        original,
    )


# Test filtering with lowercase text
def test_case_insensitive_filter(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "it",
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 70000


# Test filtering with extra whitespace
def test_filter_ignores_whitespace(sample_dataframe):
    command = {
        "operation": "count",
        "filter": {
            "column": "department",
            "value": " IT ",
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 2


# Test that numeric filtering still works
def test_numeric_filter(sample_dataframe):
    command = {
        "operation": "count",
        "filter": {
            "column": "annual_salary",
            "value": 80000,
        },
    }

    result = dispatch_command(sample_dataframe, command)

    assert result == 1