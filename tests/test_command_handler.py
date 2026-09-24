
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


# Test an invalid cleaning action
def test_invalid_action():
    command = {
        "action": "delete_everything",
        "parameters": {}
    }

    with pytest.raises(ValueError):
        parse_command(command)


# Test an unsupported operation
def test_invalid_operation():
    command = {
        "operation": "multiply",
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


# Test a command without an action or operation
def test_missing_command_type():
    command = {}

    with pytest.raises(ValueError):
        parse_command(command)


# Test a valid minimum operation
def test_valid_minimum_operation():
    command = {
        "operation": "minimum",
        "column": "annual_salary"
    }

    result = parse_command(command)

    assert result["operation"] == "minimum"
    assert result["column"] == "annual_salary"


# Test a valid maximum operation
def test_valid_maximum_operation():
    command = {
        "operation": "maximum",
        "column": "annual_salary"
    }

    result = parse_command(command)

    assert result["operation"] == "maximum"
    assert result["column"] == "annual_salary"


# Test a valid median operation
def test_valid_median_operation():
    command = {
        "operation": "median",
        "column": "annual_salary"
    }

    result = parse_command(command)

    assert result["operation"] == "median"
    assert result["column"] == "annual_salary"


# Test a grouped average command
def test_grouped_average_command():
    command = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "department",
    }

    result = parse_command(command)

    assert result == command


# Test a grouped count command
def test_grouped_count_command():
    command = {
        "operation": "count",
        "group_by": "department",
    }

    result = parse_command(command)

    assert result == command


# Test an invalid grouping column
def test_invalid_grouping_column():
    command = {
        "operation": "average",
        "column": "annual_salary",
        "group_by": "",
    }

    with pytest.raises(ValueError):
        parse_command(command)

# Test a command with both cleaning and analysis
def test_action_and_operation_together():
    command = {
        "action": "remove_duplicates",
        "operation": "average",
        "column": "annual_salary",
    }

    with pytest.raises(ValueError, match="both an action and an operation"):
        parse_command(command)


# Test invalid cleaning parameters
def test_invalid_cleaning_parameters():
    command = {
        "action": "remove_duplicates",
        "parameters": ["invalid"],
    }

    with pytest.raises(ValueError, match="Parameters must be a dictionary"):
        parse_command(command)


# Test filling missing values without a column
def test_fill_missing_values_without_column():
    command = {
        "action": "fill_missing_values",
        "parameters": {
            "value": 0,
        },
    }

    with pytest.raises(ValueError, match="valid column"):
        parse_command(command)


# Test a filter with an unsupported field
def test_filter_with_extra_field():
    command = {
        "operation": "count",
        "filter": {
            "column": "department",
            "value": "IT",
            "operator": "greater_than",
        },
    }

    with pytest.raises(ValueError, match="only a column and value"):
        parse_command(command)


# Test a filter with a missing value
def test_filter_missing_value():
    command = {
        "operation": "count",
        "filter": {
            "column": "department",
        },
    }

    with pytest.raises(ValueError, match="only a column and value"):
        parse_command(command)


# Test a filter with NaN
def test_filter_nan_value():
    command = {
        "operation": "count",
        "filter": {
            "column": "annual_salary",
            "value": float("nan"),
        },
    }

    with pytest.raises(ValueError, match="finite"):
        parse_command(command)


# Test unsupported fields in an analysis command
def test_analysis_with_unsupported_field():
    command = {
        "operation": "average",
        "column": "annual_salary",
        "execute_python": "print('hello')",
    }

    with pytest.raises(ValueError, match="unsupported fields"):
        parse_command(command)


# Test count with an unexpected column
def test_count_with_column():
    command = {
        "operation": "count",
        "column": "department",
    }

    with pytest.raises(ValueError, match="Count does not accept"):
        parse_command(command)