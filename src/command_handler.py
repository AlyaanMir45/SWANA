
import math


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

    action = command.get("action")
    operation = command.get("operation")

    # A command cannot be cleaning and analysis at once
    if action is not None and operation is not None:
        raise ValueError(
            "Command cannot contain both an action and an operation."
        )

    # Check for a cleaning action
    if action is not None:
        if action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Unsupported action: {action}"
            )

        # Reject analysis fields in cleaning commands
        invalid_fields = {
            "operation",
            "column",
            "group_by",
            "filter",
        }.intersection(command)

        if invalid_fields:
            raise ValueError(
                "Cleaning commands cannot contain analysis fields."
            )

        # Check for unsupported fields
        if set(command) - {"action", "parameters"}:
            raise ValueError(
                "Cleaning command contains unsupported fields."
            )

        parameters = command.get("parameters", {})

        # Parameters must be a dictionary
        if not isinstance(parameters, dict):
            raise ValueError(
                "Parameters must be a dictionary."
            )

        # Validate fill missing values
        if action == "fill_missing_values":
            if set(parameters) - {"column", "value"}:
                raise ValueError(
                    "Unsupported fill parameters."
                )

            column = parameters.get("column")
            value = parameters.get("value")

            if not isinstance(column, str) or not column.strip():
                raise ValueError(
                    "A valid column is required to fill missing values."
                )

            if value is None:
                raise ValueError(
                    "A replacement value is required."
                )

            if not isinstance(value, (str, int, float, bool)):
                raise ValueError(
                    "Unsupported replacement value."
                )

            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError(
                    "Replacement value must be finite."
                )

        # Other cleaning actions do not need parameters
        elif parameters:
            raise ValueError(
                f"{action} does not accept parameters."
            )

        return {
            "action": action,
            "parameters": parameters,
        }

    # Check for an analysis operation
    if operation is not None:
        if operation not in ALLOWED_OPERATIONS:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

        # Reject unsupported fields
        allowed_fields = {
            "operation",
            "column",
            "group_by",
            "filter",
        }

        if set(command) - allowed_fields:
            raise ValueError(
                "Analysis command contains unsupported fields."
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

        # Count does not need a column
        elif "column" in command:
            raise ValueError(
                "Count does not accept a column."
            )

        # Check for a grouping column
        if "group_by" in command:
            group_by = command["group_by"]

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

            # Filter must be a dictionary
            if not isinstance(filter_data, dict):
                raise ValueError(
                    "Filter must be a dictionary."
                )

            # Only one equality filter is supported
            if set(filter_data) != {"column", "value"}:
                raise ValueError(
                    "Filter must contain only a column and value."
                )

            filter_column = filter_data["column"]
            filter_value = filter_data["value"]

            # Validate the filter column
            if (
                not isinstance(filter_column, str)
                or not filter_column.strip()
            ):
                raise ValueError(
                    "A valid filter column is required."
                )

            # Validate the filter value
            if not isinstance(filter_value, (str, int, float, bool)):
                raise ValueError(
                    "A valid filter value is required."
                )

            if isinstance(filter_value, str) and not filter_value.strip():
                raise ValueError(
                    "A valid filter value is required."
                )

            # Reject NaN and infinity
            if isinstance(filter_value, float):
                if not math.isfinite(filter_value):
                    raise ValueError(
                        "Filter value must be finite."
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