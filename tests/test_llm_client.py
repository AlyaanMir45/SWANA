
import json
from unittest.mock import patch, MagicMock

import pytest

from src.llm_client import (
    generate_command,
    CommandGenerationError,
)


# Test a valid average command
@patch("src.llm_client.client.responses.create")
def test_generate_average_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "average",
        "column": "annual_salary",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the average annual salary?",
        ["annual_salary"],
    )

    assert result == {
        "operation": "average",
        "column": "annual_salary",
    }

    mock_create.assert_called_once()


# Test a valid minimum command
@patch("src.llm_client.client.responses.create")
def test_generate_minimum_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "minimum",
        "column": "annual_salary",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the minimum annual salary?",
        ["annual_salary"],
    )

    assert result["operation"] == "minimum"
    assert result["column"] == "annual_salary"


# Test a valid maximum command
@patch("src.llm_client.client.responses.create")
def test_generate_maximum_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "maximum",
        "column": "annual_salary",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the maximum annual salary?",
        ["annual_salary"],
    )

    assert result["operation"] == "maximum"
    assert result["column"] == "annual_salary"


# Test a valid median command
@patch("src.llm_client.client.responses.create")
def test_generate_median_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "median",
        "column": "annual_salary",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the median annual salary?",
        ["annual_salary"],
    )

    assert result["operation"] == "median"
    assert result["column"] == "annual_salary"


# Test invalid JSON on both attempts
@patch("src.llm_client.client.responses.create")
def test_invalid_json_response(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = "This is not JSON"

    mock_create.return_value = mock_response

    with pytest.raises(CommandGenerationError):
        generate_command(
            "What is the average annual salary?",
            ["annual_salary"],
        )

    assert mock_create.call_count == 2


# Test an API failure
@patch("src.llm_client.client.responses.create")
def test_api_failure(mock_create):
    mock_create.side_effect = RuntimeError(
        "Groq API unavailable"
    )

    with pytest.raises(RuntimeError):
        generate_command(
            "What is the average annual salary?",
            ["annual_salary"],
        )

    # API failures are not retried by our current implementation
    mock_create.assert_called_once()


# Test a grouped average command
@patch("src.llm_client.client.responses.create")
def test_grouped_average_prompt(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "average",
        "column": "annual_salary",
        "group_by": "department",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the average annual salary by department?",
        ["annual_salary", "department"],
    )

    assert result["operation"] == "average"
    assert result["column"] == "annual_salary"
    assert result["group_by"] == "department"

    prompt = mock_create.call_args.kwargs["input"]

    assert "group_by" in prompt
    assert "department" in prompt


# Test a grouped sum command
@patch("src.llm_client.client.responses.create")
def test_grouped_sum_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "sum",
        "column": "annual_salary",
        "group_by": "department",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "What is the total annual salary by department?",
        ["annual_salary", "department"],
    )

    assert result == {
        "operation": "sum",
        "column": "annual_salary",
        "group_by": "department",
    }


# Test a grouped count command
@patch("src.llm_client.client.responses.create")
def test_grouped_count_command(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = json.dumps({
        "operation": "count",
        "group_by": "department",
    })

    mock_create.return_value = mock_response

    result = generate_command(
        "How many employees are in each department?",
        ["department"],
    )

    assert result == {
        "operation": "count",
        "group_by": "department",
    }


# Test recovery when the second attempt returns valid JSON
@patch("src.llm_client.client.responses.create")
def test_retry_succeeds(mock_create):
    invalid_response = MagicMock()
    invalid_response.output_text = "Invalid JSON"

    valid_response = MagicMock()
    valid_response.output_text = json.dumps({
        "operation": "average",
        "column": "annual_salary",
    })

    mock_create.side_effect = [
        invalid_response,
        valid_response,
    ]

    result = generate_command(
        "What is the average annual salary?",
        ["annual_salary"],
    )

    assert result == {
        "operation": "average",
        "column": "annual_salary",
    }

    assert mock_create.call_count == 2


# Test empty commands on both attempts
@patch("src.llm_client.client.responses.create")
def test_empty_command_retries(mock_create):
    mock_response = MagicMock()
    mock_response.output_text = "{}"

    mock_create.return_value = mock_response

    with pytest.raises(
        CommandGenerationError,
        match="SWANA could not understand",
    ):
        generate_command(
            "Do something unsupported",
            ["annual_salary"],
        )

    assert mock_create.call_count == 2