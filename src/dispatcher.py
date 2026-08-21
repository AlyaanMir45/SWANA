from src.executor import execute_operation
from src.cleaner import (
    remove_duplicates,
    remove_missing_rows,
    fill_missing_values,
    remove_empty_columns,
    standardize_column_names,
)


def dispatch_command(dataframe, command):
    # Check for an analysis command
    if "operation" in command:
        return execute_operation(dataframe, command)

    # Get the cleaning action
    action = command.get("action")

    # Run the matching cleaning function
    if action == "remove_duplicates":
        return remove_duplicates(dataframe)

    elif action == "remove_missing_rows":
        return remove_missing_rows(dataframe)

    elif action == "fill_missing_values":
        parameters = command.get("parameters", {})
        value = parameters.get("value")

        return fill_missing_values(
            dataframe,
            value,
        )

    elif action == "remove_empty_columns":
        return remove_empty_columns(dataframe)

    elif action == "standardize_column_names":
        return standardize_column_names(dataframe)

    # The command was not recognized
    raise ValueError("Invalid command.")