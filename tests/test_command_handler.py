import pytest

from src.command_handler import parse_command


# Test a valid cleaning action
def test_valid_cleaning_action():
    command = {
        "action": "remove_duplicates",
        "parameters": {}
    }

    result = parse_command(command)

    assert result["action"] == "remove_duplicates"
    assert result["parameters"] == {}


# Test a valid average operation
def test_valid_average_operation():
    command = {
        "operation": "average",
        "column": "annual_salary"
    }

    result = parse_command(command)

    assert result["operation"] == "average"
    assert result["column"] == "annual_salary"


# Test a valid sum operation
def test_valid_sum_operation():
    command = {
        "operation": "sum",
        "column": "annual_salary"
    }

    result = parse_command(command)

    assert result["operation"] == "sum"
    assert result["column"] == "annual_salary"


# Test a valid count operation
def test_valid_count_operation():
    command = {
        "operation": "count"
    }

    result = parse_command(command)

    assert result["operation"] == "count"


# Test an unsupported cleaning action
def test_invalid_action():
    command = {
        "action": "delete_everything"
    }

    with pytest.raises(ValueError):
        parse_command(command)


# Test an unsupported analysis operation
def test_invalid_operation():
    command = {
        "operation": "median",
        "column": "annual_salary"
    }

    with pytest.raises(ValueError):
        parse_command(command)


# Test average without a column
def test_average_without_column():
    command = {
        "operation": "average"
    }

    with pytest.raises(ValueError):
        parse_command(command)


# Test sum without a column
def test_sum_without_column():
    command = {
        "operation": "sum"
    }

    with pytest.raises(ValueError):
        parse_command(command)


# Test a command with no action or operation
def test_missing_command_type():
    command = {}

    with pytest.raises(ValueError):
        parse_command(command)