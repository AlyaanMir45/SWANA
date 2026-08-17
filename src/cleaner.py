import pandas as pd


def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the dataset.
    """
    cleaned_dataframe = dataframe.drop_duplicates()

    return cleaned_dataframe


def remove_missing_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that contain missing values.
    """
    cleaned_dataframe = dataframe.dropna()

    return cleaned_dataframe


def fill_missing_values(
    dataframe: pd.DataFrame,
    value
) -> pd.DataFrame:
    """
    Fill missing values in the dataset.
    """
    cleaned_dataframe = dataframe.fillna(value)

    return cleaned_dataframe


def remove_empty_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove columns that contain only missing values.
    """
    cleaned_dataframe = dataframe.dropna(axis=1, how="all")

    return cleaned_dataframe


def standardize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names.
    """
    cleaned_dataframe = dataframe.copy()

    cleaned_dataframe.columns = (
        cleaned_dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return cleaned_dataframe