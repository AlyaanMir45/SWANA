
import pandas as pd
import pytest

from src.graphmaker import prepare_grouped_chart


# Create sample grouped data for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "department": ["IT", "HR", "Sales"],
        "sum": [170000, 125000, 70000],
        "average": [85000, 62500, 70000],
    })


# Test preparing grouped sum results
def test_grouped_sum(sample_data):
    result = prepare_grouped_chart(
        sample_data,
        "department",
        "sum",
    )

    assert result.loc["IT", "sum"] == 170000
    assert result.loc["HR", "sum"] == 125000


# Test preparing grouped average results
def test_grouped_average(sample_data):
    result = prepare_grouped_chart(
        sample_data,
        "department",
        "average",
    )

    assert result.loc["IT", "average"] == 85000
    assert result.loc["HR", "average"] == 62500


# Test that all groups are included
def test_all_groups_included(sample_data):
    result = prepare_grouped_chart(
        sample_data,
        "department",
        "sum",
    )

    assert set(result.index) == {
        "IT", "HR", "Sales"
    }


# Test an invalid grouping column
def test_invalid_group_column(sample_data):
    with pytest.raises(ValueError):
        prepare_grouped_chart(
            sample_data,
            "invalid_column",
            "sum",
        )


# Test an invalid result column
def test_invalid_value_column(sample_data):
    with pytest.raises(ValueError):
        prepare_grouped_chart(
            sample_data,
            "department",
            "invalid_column",
        )


# Test that non-numeric results are rejected
def test_non_numeric_result():
    data = pd.DataFrame({
        "department": ["IT", "HR"],
        "status": ["Active", "Inactive"],
    })

    with pytest.raises(ValueError):
        prepare_grouped_chart(
            data,
            "department",
            "status",
        )