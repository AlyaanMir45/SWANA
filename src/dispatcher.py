
import pandas as pd

from src.executor import execute_operation
from src.grouped_analyzer import execute_grouped_operation

from src.cleaner import (
    remove_duplicates,
    remove_missing_rows,
    fill_missing_values,
    remove_empty_columns,
    standardize_column_names,
)


def dispatch_command(
    dataframe: pd.DataFrame,
    command: dict,
):
    """
    Route a validated command to the appropriate
    cleaning or analysis function.
    """

    # Get the operation and action from the command
    operation = command.get("operation")
    action = command.get("action")

    # Apply filters to analysis commands
    if operation is not None and "filter" in command:
        filter_data = command["filter"]

        filter_column = filter_data["column"]
        filter_value = filter_data["value"]

        # Check that the filter column exists
        if filter_column not in dataframe.columns:
            raise ValueError(
                f"Filter column '{filter_column}' was not found."
            )

        # Filter the dataset without changing the original
        dataframe = dataframe.loc[
            dataframe[filter_column] == filter_value
        ].copy()

        # Check whether any matching rows were found
        if dataframe.empty:
            raise ValueError(
                f"No rows found where "
                f"{filter_column} equals {filter_value}."
            )

    # Execute grouped analysis first
    if operation is not None and "group_by" in command:
        return execute_grouped_operation(
            dataframe,
            command,
        )

    # Execute regular analysis
    if operation is not None:
        return execute_operation(
            dataframe,
            command,
        )

    # Get any parameters for cleaning operations
    parameters = command.get("parameters", {})

    # Remove duplicate rows
    if action == "remove_duplicates":
        return remove_duplicates(dataframe)

    # Remove rows containing missing values
    elif action == "remove_missing_rows":
        return remove_missing_rows(dataframe)

    # Fill missing values in a specified column
    elif action == "fill_missing_values":
        column = parameters.get("column")
        value = parameters.get("value")

        return fill_missing_values(
            dataframe,
            column,
            value,
        )

    # Remove completely empty columns
    elif action == "remove_empty_columns":
        return remove_empty_columns(dataframe)

    # Standardize column names
    elif action == "standardize_column_names":
        return standardize_column_names(dataframe)

    # Reject commands that do not match any operation
    raise ValueError(
        "Invalid command."
    )