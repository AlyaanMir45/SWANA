ALLOWED_ACTIONS = {
    "remove_duplicates",
    "remove_missing_rows",
    "fill_missing_values",
    "remove_empty_columns",
    "standardize_column_names",
}


def parse_command(command: dict) -> dict:
    action = command.get("action")

    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Unsupported action: {action}")

    parameters = command.get("parameters", {})

    return {
        "action": action,
        "parameters": parameters,
    }