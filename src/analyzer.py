import pandas as pd


def get_dataset_summary(dataframe: pd.DataFrame) -> dict:
    """
    Generate a basic summary of the dataset.
    """

    # Get total rows and columns
    total_rows = dataframe.shape[0]
    total_columns = dataframe.shape[1]

    # Count all missing values
    missing_values = int(
        dataframe.isna().sum().sum()
    )

    # Count duplicate rows
    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    # Count numeric columns
    numeric_columns = len(
        dataframe.select_dtypes(include="number").columns
    )

    # Count text columns
    text_columns = len(
        dataframe.select_dtypes(include=["object", "string"]).columns
    )

    # Store the results
    summary = {
        "rows": total_rows,
        "columns": total_columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numeric_columns": numeric_columns,
        "text_columns": text_columns,
    }

    # Return the results
    return summary


def get_column_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Generate information about each column.
    """

    # Create a summary for each column
    column_summary = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Data Type": dataframe.dtypes.astype(str).values,
            "Missing Values": dataframe.isna().sum().values,
            "Unique Values": dataframe.nunique().values,
        }
    )

    # Return the column summary
    return column_summary


def get_data_quality(dataframe):
    """
    Find basic data quality problems.
    """

    # Store columns that have missing values
    missing_by_column = {}

    # Check every column
    for column in dataframe.columns:

        # Count missing values in the column
        missing_count = dataframe[column].isna().sum()

        # Save the column if it has missing values
        if missing_count:
            missing_by_column[column] = int(missing_count)

    # Count duplicate rows
    duplicate_count = int(
        dataframe.duplicated().sum()
    )

    # Store the data quality results
    quality_report = {
        "missing_by_column": missing_by_column,
        "duplicate_rows": duplicate_count,
    }

    # Return the results
    return quality_report