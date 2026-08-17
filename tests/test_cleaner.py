import pandas as pd

# Import cleaning functions
from src.cleaner import (
    remove_duplicates,
    remove_missing_rows,
    fill_missing_values,
    remove_empty_columns,
    standardize_column_names,
)


def test_remove_duplicates():
    # Create data with one duplicate row
    test_data = pd.DataFrame({
        "Name": ["Ali", "Bob", "Ali"],
        "Age": [21, 67, 21]
    })

    cleaned_data = remove_duplicates(test_data)

    # One duplicate should be removed
    assert len(cleaned_data) == 2


def test_remove_missing_rows():
    # Create data with missing values
    test_data = pd.DataFrame({
        "Name": ["Ali", "Bob", None],
        "Age": [21, None, 30]
    })

    cleaned_data = remove_missing_rows(test_data)

    # Only the complete row should remain
    assert len(cleaned_data) == 1


def test_fill_missing_values():
    # Create data with a missing age
    test_data = pd.DataFrame({
        "Name": ["Ali", "Bob", "Sara"],
        "Age": [21, None, 24]
    })

    cleaned_data = fill_missing_values(test_data, 0)

    # Missing value should become 0
    assert cleaned_data["Age"].isna().sum() == 0
    assert cleaned_data.loc[1, "Age"] == 0


def test_remove_empty_columns():
    # Create one completely empty column
    test_data = pd.DataFrame({
        "Name": ["Ali", "Bob", "Sara"],
        "Age": [21, 25, 24],
        "Notes": [None, None, None]
    })

    cleaned_data = remove_empty_columns(test_data)

    # Empty Notes column should be removed
    assert "Notes" not in cleaned_data.columns


def test_standardize_column_names():
    # Create messy column names
    test_data = pd.DataFrame({
        " First Name ": ["Ali"],
        "Last Name": ["Mir"],
        "AGE": [21]
    })

    cleaned_data = standardize_column_names(test_data)

    # Column names should be cleaned
    assert list(cleaned_data.columns) == [
        "first_name",
        "last_name",
        "age"
    ]