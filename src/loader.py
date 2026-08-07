from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_dataset(uploaded_file) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Args:
        uploaded_file: File uploaded through Streamlit.

    Returns:
        A pandas DataFrame.

    Raises:
        ValueError: If the file type is unsupported.
    """
    file_extension = Path(uploaded_file.name).suffix.lower()

    if file_extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Please upload a CSV or Excel file."
        )

    if file_extension == ".csv":
        return load_csv(uploaded_file)

    return load_excel(uploaded_file)


def load_csv(uploaded_file) -> pd.DataFrame:
    """Load a CSV file and handle common encoding issues."""
    try:
        return pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="latin-1")


def load_excel(uploaded_file) -> pd.DataFrame:
    """Load an Excel file."""
    return pd.read_excel(uploaded_file)