
import pandas as pd


def prepare_grouped_chart(
    result: pd.DataFrame,
    group_by: str,
    operation: str,
) -> pd.DataFrame:
    """
    Prepare grouped analysis results for visualization.

    Returns a new DataFrame indexed by the grouping column,
    with the analysis result as its numeric value.
    """

    # Check that the grouping column exists
    if group_by not in result.columns:
        raise ValueError(
            f"Grouping column '{group_by}' was not found."
        )

    # Check that the operation column exists
    if operation not in result.columns:
        raise ValueError(
            f"Result column '{operation}' was not found."
        )

    # Ensure the result can be plotted
    if not pd.api.types.is_numeric_dtype(result[operation]):
        raise ValueError(
            "The analysis result must be numeric."
        )

    # Prepare a separate DataFrame without changing the result
    chart_data = result[[group_by, operation]].copy()

    return chart_data.set_index(group_by)