
import pandas as pd
import pytest

from src.grouped_analyzer import execute_grouped_operation


# Create a sample dataset for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "department": ["IT", "IT", "Finance", "Finance"],
        "annual_salary": [60000, 80000, 70000, 90000],
    })


# Test grouped average
def test_grouped_average(sample_dataframe):
    instruction = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "department",
    }

    result = execute_grouped_operation(
        sample_dataframe,
        instruction,
    )

    assert result.loc[
        result["department"] == "IT", "average"
    ].iloc[0] == 70000

    assert result.loc[
        result["department"] == "Finance", "average"
    ].iloc[0] == 80000


# Test grouped sum
def test_grouped_sum(sample_dataframe):
    instruction = {
        "operation": "sum",
        "column": "annual_salary",
        "group_by": "department",
    }

    result = execute_grouped_operation(
        sample_dataframe,
        instruction,
    )

    assert result.loc[
        result["department"] == "IT", "sum"
    ].iloc[0] == 140000


# Test grouped count
def test_grouped_count(sample_dataframe):
    instruction = {
        "operation": "count",
        "group_by": "department",
    }

    result = execute_grouped_operation(
        sample_dataframe,
        instruction,
    )

    assert result.loc[
        result["department"] == "IT", "count"
    ].iloc[0] == 2


# Test an invalid grouping column
def test_invalid_grouping_column(sample_dataframe):
    instruction = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "unknown",
    }

    with pytest.raises(ValueError):
        execute_grouped_operation(
            sample_dataframe,
            instruction,
        )


# Test an unsupported grouped operation
def test_unsupported_grouped_operation(sample_dataframe):
    instruction = {
        "operation": "multiply",
        "column": "annual_salary",
        "group_by": "department",
    }

    with pytest.raises(ValueError):
        execute_grouped_operation(
            sample_dataframe,
            instruction,
        )