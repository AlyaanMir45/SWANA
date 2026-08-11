import pandas as pd
import streamlit as st

from src.loader import load_dataset
from src.analyzer import (
    get_dataset_summary,
    get_column_summary,
    get_data_quality,
)


# Configure the browser tab and page layout

st.set_page_config(
    page_title="SWANA",
    layout="wide",
)


# Page header

st.title("SWANA")
st.subheader("Smart Web Analytics & Narrative Assistant")

st.write(
    "Upload a CSV or Excel dataset to explore its structure, "
    "preview its contents, and view basic statistics."
)


# File uploader

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)


if uploaded_file is None:
    st.info("Upload a CSV or Excel file to begin.")

else:
    try:
        # Load the uploaded dataset
        dataframe = load_dataset(uploaded_file)

        # Analyze the dataset
        summary = get_dataset_summary(dataframe)
        column_information = get_column_summary(dataframe)
        quality_report = get_data_quality(dataframe)

        # Get data quality results
        missing_by_column = quality_report["missing_by_column"]
        duplicate_rows = quality_report["duplicate_rows"]

        st.success(f"Successfully loaded: {uploaded_file.name}")


        # Dataset overview

        st.header("Dataset Overview")

        column1, column2, column3 = st.columns(3)

        with column1:
            st.metric(
                "Rows",
                f"{summary['rows']:,}"
            )

        with column2:
            st.metric(
                "Columns",
                summary["columns"]
            )

        with column3:
            st.metric(
                "Missing Values",
                f"{summary['missing_values']:,}"
            )


        column4, column5, column6 = st.columns(3)

        with column4:
            st.metric(
                "Duplicate Rows",
                f"{summary['duplicate_rows']:,}"
            )

        with column5:
            st.metric(
                "Numeric Columns",
                summary["numeric_columns"]
            )

        with column6:
            st.metric(
                "Text Columns",
                summary["text_columns"]
            )


        # Data quality

        st.header("Data Quality")

        # Show missing value problems
        if missing_by_column:
            st.warning("Missing values were detected.")

            for column, missing_count in missing_by_column.items():
                st.write(
                    f"{column}: {missing_count} missing value(s)"
                )

        else:
            st.success("No missing values were detected.")


        # Show duplicate row problems
        if duplicate_rows:
            st.warning(
                f"{duplicate_rows} duplicate row(s) were detected."
            )

        else:
            st.success("No duplicate rows were detected.")


        # Dataset preview

        st.header("Data Preview")

        preview_rows = st.slider(
            "Number of rows to display",
            min_value=5,
            max_value=min(100, len(dataframe)),
            value=min(10, len(dataframe)),
        )

        st.dataframe(
            dataframe.head(preview_rows),
            use_container_width=True,
        )


        # Column information

        st.header("Column Information")

        st.dataframe(
            column_information,
            use_container_width=True,
            hide_index=True,
        )


        # Numeric statistics

        numeric_columns = dataframe.select_dtypes(
            include="number"
        )

        if not numeric_columns.empty:
            st.header("Numeric Summary")

            st.dataframe(
                numeric_columns.describe().transpose(),
                use_container_width=True,
            )

        else:
            st.info(
                "This dataset does not contain numeric columns."
            )


    except pd.errors.EmptyDataError:
        st.error(
            "The uploaded file is empty."
        )

    except pd.errors.ParserError:
        st.error(
            "The uploaded file could not be read. "
            "Check its formatting."
        )

    except Exception as error:
        st.error(
            f"An unexpected error occurred: {error}"
        )