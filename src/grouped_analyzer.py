
import pandas as pd


def execute_grouped_operation(
    dataframe: pd.DataFrame,
    instruction: dict,
):
    """
    Execute a grouped data analysis operation.
    """

    # Get values from the instruction
    operation = instruction.get("operation")
    column = instruction.get("column")
    group_by = instruction.get("group_by")

    # List supported grouped operations
    supported_operations = [
        "average",
        "sum",
        "count",
    ]

    # Check that the operation is supported
    if operation not in supported_operations:
        raise ValueError(
            f"Unsupported grouped operation: {operation}"
        )

    # Check that the grouping column exists
    if group_by not in dataframe.columns:
        raise ValueError(
            f"Grouping column '{group_by}' was not found."
        )

    # Check the numeric column when required
    if operation != "count":
        if column not in dataframe.columns:
            raise ValueError(
                f"Column '{column}' was not found."
            )

        if not pd.api.types.is_numeric_dtype(dataframe[column]):
            raise ValueError(
                f"Column '{column}' must be numeric."
            )

    # Calculate the grouped average
    if operation == "average":
        result = dataframe.groupby(group_by)[column].mean()

    # Calculate the grouped sum
    elif operation == "sum":
        result = dataframe.groupby(group_by)[column].sum()

    # Count rows in each group
    elif operation == "count":
        result = dataframe.groupby(group_by).size()

    # Convert the results into a dataframe
    return result.reset_index(
        name=operation
    )