
# Cleaning actions SWANA supports
ALLOWED_ACTIONS = {
    "remove_duplicates",
    "remove_missing_rows",
    "fill_missing_values",
    "remove_empty_columns",
    "standardize_column_names",
}

# Analysis operations SWANA supports
ALLOWED_OPERATIONS = {
    "average",
    "sum",
    "count",
    "minimum",
    "maximum",
    "median",
}

# Operations supported by grouped analysis
GROUPED_OPERATIONS = {
    "average",
    "sum",
    "count",
}


def parse_command(command: dict) -> dict:
    # Check that the command is a dictionary
    if not isinstance(command, dict):
        raise ValueError(
            "Command must be a dictionary."
        )

    # Check for a cleaning action
    action = command.get("action")

    if action is not None:
        if action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Unsupported action: {action}"
            )

        parameters = command.get("parameters", {})

        return {
            "action": action,
            "parameters": parameters,
        }

    # Check for an analysis operation
    operation = command.get("operation")

    if operation is not None:
        if operation not in ALLOWED_OPERATIONS:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

        parsed_command = {
            "operation": operation,
        }

        # All operations except count need a column
        if operation != "count":
            column = command.get("column")

            if not isinstance(column, str) or not column.strip():
                raise ValueError(
                    f"{operation} requires a column."
                )

            parsed_command["column"] = column

        # Check for a grouping column
        group_by = command.get("group_by")

        if group_by is not None:
            if not isinstance(group_by, str) or not group_by.strip():
                raise ValueError(
                    "A valid grouping column is required."
                )

            # Only supported operations can be grouped
            if operation not in GROUPED_OPERATIONS:
                raise ValueError(
                    f"Grouped {operation} is not supported."
                )

            parsed_command["group_by"] = group_by

        # Check for a filter
        if "filter" in command:
            filter_data = command["filter"]

            # Filter must contain a column and value
            if not isinstance(filter_data, dict):
                raise ValueError(
                    "Filter must be a dictionary."
                )

            filter_column = filter_data.get("column")
            filter_value = filter_data.get("value")

            # Validate the filter column
            if (
                not isinstance(filter_column, str)
                or not filter_column.strip()
            ):
                raise ValueError(
                    "A valid filter column is required."
                )

            # Validate the filter value
            if (
                not isinstance(filter_value, (str, int, float, bool))
                or isinstance(filter_value, str)
                and not filter_value.strip()
            ):
                raise ValueError(
                    "A valid filter value is required."
                )

            parsed_command["filter"] = {
                "column": filter_column,
                "value": filter_value,
            }

        return parsed_command

    # No valid command type was found
    raise ValueError(
        "Command must include an action or operation."
    )