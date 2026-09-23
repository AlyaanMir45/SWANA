import pandas as pd
import pytest

# Import the executor
from src.executor import execute_operation


def test_average():
    # Create test data
    test_data = pd.DataFrame({
        "Order Amount": [100, 200, 300]
    })

    # Create the instruction
    instruction = {
        "operation": "average",
        "column": "Order Amount"
    }

    # Execute the instruction
    result = execute_operation(test_data, instruction)

    # Average should be 200
    assert result == 200


def test_sum():
    # Create test data
    test_data = pd.DataFrame({
        "Order Amount": [100, 200, 300]
    })

    # Create the instruction
    instruction = {
        "operation": "sum",
        "column": "Order Amount"
    }

    # Execute the instruction
    result = execute_operation(test_data, instruction)

    # Total should be 600
    assert result == 600


def test_count():
    # Create test data with three rows
    test_data = pd.DataFrame({
        "Name": ["Ali", "Bob", "Sara"]
    })

    # Create the instruction
    instruction = {
        "operation": "count"
    }

    # Execute the instruction
    result = execute_operation(test_data, instruction)

    # Dataset should contain three rows
    assert result == 3


def test_invalid_column():
    # Create test data
    test_data = pd.DataFrame({
        "Order Amount": [100, 200, 300]
    })

    # Ask for a column that does not exist
    instruction = {
        "operation": "average",
        "column": "Revenue"
    }

    # Make sure an invalid column is rejected
    with pytest.raises(ValueError):
        execute_operation(test_data, instruction)


def test_unsupported_operation():
    # Create test data
    test_data = pd.DataFrame({
        "Order Amount": [100, 200, 300]
    })

    # Ask for an unsupported operation
    instruction = {
        "operation": "delete",
        "column": "Order Amount"
    }

    # Make sure unsupported operations are rejected
    with pytest.raises(ValueError):
        execute_operation(test_data, instruction)


# Test the minimum operation
def test_minimum_operation():
    dataframe = pd.DataFrame({
        "annual_salary": [50000, 75000, 100000]
    })

    instruction = {
        "operation": "minimum",
        "column": "annual_salary"
    }

    result = execute_operation(dataframe, instruction)

    assert result == 50000


# Test the maximum operation
def test_maximum_operation():
    dataframe = pd.DataFrame({
        "annual_salary": [50000, 75000, 100000]
    })

    instruction = {
        "operation": "maximum",
        "column": "annual_salary"
    }

    result = execute_operation(dataframe, instruction)

    assert result == 100000


# Test the median operation
def test_median_operation():
    dataframe = pd.DataFrame({
        "annual_salary": [50000, 75000, 100000]
    })

    instruction = {
        "operation": "median",
        "column": "annual_salary"
    }

    result = execute_operation(dataframe, instruction)

    assert result == 75000