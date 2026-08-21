# Actions and phrases the interpreter understands
COMMANDS = {
    "remove_duplicates": [
        "duplicate",
        "duplicates",
        "duplicate rows",
    ],
    "remove_missing_rows": [
        "missing rows",
        "rows with missing values",
    ],
    "remove_empty_columns": [
        "empty columns",
        "blank columns",
    ],
    "standardize_column_names": [
        "column names",
        "standardize columns",
    ],
}


def interpret_request(user_request: str) -> dict:
    # Make the request lowercase
    request = user_request.lower()

    # Look for a matching command
    for action, keywords in COMMANDS.items():
        if any(keyword in request for keyword in keywords):
            return {
                "action": action,
                "parameters": {},
            }

    # No matching command was found
    raise ValueError("Could not understand request.")