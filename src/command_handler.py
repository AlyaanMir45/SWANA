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
}


def parse_command(command: dict) -> dict:
    # Check for a cleaning action
    action = command.get("action")

    if action is not None:
        if action not in ALLOWED_ACTIONS:
            raise ValueError(f"Unsupported action: {action}")

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

        # Average and sum need a column
        if operation != "count":
            column = command.get("column")

            if not column:
                raise ValueError(
                    f"{operation} requires a column."
                )

            parsed_command["column"] = column

        return parsed_command

    # No valid command type was found
    raise ValueError("Command must include an action or operation.")