import pandas as pd


def execute_operation(
    dataframe: pd.DataFrame,
    instruction: dict,
):
    """
    Execute a data operation.
    """

    # Get values from the instruction
    operation = instruction.get("operation")
    column = instruction.get("column")

    # List the supported operations
    supported_operations = [
        "average",
        "sum",
        "count",
    ]

    # Check that the operation is supported
    if operation not in supported_operations:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    # Check the column for operations that need one
    if operation != "count":
        if column not in dataframe.columns:
            raise ValueError(
                f"Column '{column}' was not found."
            )

    # Calculate the average
    if operation == "average":
        return dataframe[column].mean()

    # Calculate the sum
    elif operation == "sum":
        return dataframe[column].sum()

    # Count the rows
    elif operation == "count":
        return len(dataframe)