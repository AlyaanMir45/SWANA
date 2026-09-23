
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


# Analysis operations and their keywords
OPERATIONS = {
    "average": ["average", "mean"],
    "sum": ["sum", "total"],
    "minimum": ["minimum", "lowest", "smallest", "min"],
    "maximum": ["maximum", "highest", "largest", "max"],
    "median": ["median"],
}


def interpret_request(user_request: str) -> dict:
    # Make the request lowercase
    request = user_request.lower()

    # Check for a count request
    if "count" in request:
        return {
            "operation": "count",
        }

    # Check for an analysis operation
    for operation, keywords in OPERATIONS.items():
        for keyword in keywords:
            if keyword in request:
                column = request.replace("what is the", "")
                column = column.replace("calculate the", "")
                column = column.replace("find the", "")
                column = column.replace(keyword, "")
                column = column.replace("of", "")
                column = column.replace("?", "")
                column = column.strip()
                column = column.replace(" ", "_")

                return {
                    "operation": operation,
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