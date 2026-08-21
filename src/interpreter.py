# Cleaning actions and phrases the interpreter understands
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

    # Check for a count request
    if "count" in request:
        return {
            "operation": "count",
        }

    # Check for an average request
    if "average" in request:
        column = request.replace("what is the", "")
        column = column.replace("average", "")
        column = column.replace("of", "")
        column = column.replace("?", "")
        column = column.strip()
        column = column.replace(" ", "_")

        return {
            "operation": "average",
            "column": column,
        }

    # Check for a sum request
    if "sum" in request:
        column = request.replace("what is the", "")
        column = column.replace("sum", "")
        column = column.replace("of", "")
        column = column.replace("?", "")
        column = column.strip()
        column = column.replace(" ", "_")

        return {
            "operation": "sum",
            "column": column,
        }

    # Look for a matching cleaning command
    for action, keywords in COMMANDS.items():
        if any(keyword in request for keyword in keywords):
            return {
                "action": action,
                "parameters": {},
            }

    # No matching command was found
    raise ValueError("Could not understand request.")