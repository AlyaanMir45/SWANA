import pandas as pd
import streamlit as st


# Configure the browser tab and page layout
st.set_page_config(
    page_title="SWANA",
    page_icon="📊",
    layout="wide",
)


def load_csv(uploaded_file) -> pd.DataFrame:
    """Load an uploaded CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        # Some CSV files use a different text encoding
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="latin-1")


# Page header
st.title("📊 SWANA")
st.subheader("Smart Web Analytics & Narrative Assistant")

st.write(
    "Upload a CSV dataset to explore its structure, preview its contents, "
    "and view basic statistics."
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
else:
    try:
        dataframe = load_csv(uploaded_file)

        st.success(f"Successfully loaded: {uploaded_file.name}")

        # Dataset overview
        st.header("Dataset Overview")

        column1, column2, column3 = st.columns(3)

        with column1:
            st.metric("Rows", f"{dataframe.shape[0]:,}")

        with column2:
            st.metric("Columns", dataframe.shape[1])

        with column3:
            missing_values = int(dataframe.isna().sum().sum())
            st.metric("Missing Values", f"{missing_values:,}")

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

        column_information = pd.DataFrame(
            {
                "Column": dataframe.columns,
                "Data Type": dataframe.dtypes.astype(str).values,
                "Missing Values": dataframe.isna().sum().values,
                "Unique Values": dataframe.nunique().values,
            }
        )

        st.dataframe(
            column_information,
            use_container_width=True,
            hide_index=True,
        )

        # Numeric statistics
        numeric_columns = dataframe.select_dtypes(include="number")

        if not numeric_columns.empty:
            st.header("Numeric Summary")

            st.dataframe(
                numeric_columns.describe().transpose(),
                use_container_width=True,
            )
        else:
            st.info("This dataset does not contain numeric columns.")

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")

    except pd.errors.ParserError:
        st.error("The CSV file could not be read. Check its formatting.")

    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")