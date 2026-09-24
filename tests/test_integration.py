
import pandas as pd
import pytest

from src.command_handler import parse_command
from src.dispatcher import dispatch_command


# Create a dataset for integration testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "department": [
            "IT",
            "IT",
            "Finance",
            "Finance",
        ],
        "annual_salary": [
            60000,
            80000,
            70000,
            90000,
        ],
    })


# Test the complete regular-analysis pipeline
def test_regular_analysis_pipeline(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
    }

    validated_command = parse_command(command)

    result = dispatch_command(
        sample_dataframe,
        validated_command,
    )

    assert result == 75000


# Test the complete grouped-analysis pipeline
def test_grouped_analysis_pipeline(sample_dataframe):
    command = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "department",
    }

    validated_command = parse_command(command)

    result = dispatch_command(
        sample_dataframe,
        validated_command,
    )

    assert result.loc[
        result["department"] == "IT",
        "average",
    ].iloc[0] == 70000

    assert result.loc[
        result["department"] == "Finance",
        "average",
    ].iloc[0] == 80000


# Verify grouped analysis does not modify the dataset
def test_grouped_analysis_preserves_dataset(
    sample_dataframe,
):
    original_dataframe = sample_dataframe.copy(deep=True)

    command = {
        "operation": "sum",
        "column": "annual_salary",
        "group_by": "department",
    }

    validated_command = parse_command(command)

    dispatch_command(
        sample_dataframe,
        validated_command,
    )

    pd.testing.assert_frame_equal(
        sample_dataframe,
        original_dataframe,
    )


# Test that invalid commands are rejected
def test_invalid_command_pipeline(sample_dataframe):
    command = {
        "operation": "multiply",
        "column": "annual_salary",
    }

    with pytest.raises(ValueError):
        validated_command = parse_command(command)

        dispatch_command(
            sample_dataframe,
            validated_command,
        )

# Test the complete natural-language filtering pipeline
def test_filtered_analysis_pipeline():
    import json
    from unittest.mock import patch, MagicMock

    import pandas as pd

    from src.llm_client import generate_command
    from src.command_handler import parse_command
    from src.dispatcher import dispatch_command

    dataframe = pd.DataFrame({
        "department": ["IT", "IT", "Finance", "Finance"],
        "annual_salary": [60000, 80000, 70000, 90000],
    })

    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "average",
        "column": "annual_salary",
        "filter": {
            "column": "department",
            "value": "IT",
        },
    })

    with patch(
        "src.llm_client.client.responses.create",
        return_value=mock_response,
    ):
        command = generate_command(
            "What is the average salary of the IT department?",
            dataframe.columns.tolist(),
        )

    parsed_command = parse_command(command)

    result = dispatch_command(
        dataframe,
        parsed_command,
    )

    assert result == 70000