
import pandas as pd
import streamlit as st

from src.loader import load_dataset
from src.analyzer import (
    get_dataset_summary,
    get_column_summary,
    get_data_quality,
)
from src.cleaner import (
    remove_duplicates,
    remove_missing_rows,
    remove_empty_columns,
    standardize_column_names,
)
from src.llm_client import (
    generate_command,
    CommandGenerationError,
)
from src.command_handler import parse_command
from src.dispatcher import dispatch_command
from src.graphmaker import prepare_grouped_chart


# Configure the browser tab and page layout

st.set_page_config(
    page_title="SWANA",
    page_icon="📊",
    layout="wide",
)


# Helper functions

def clear_analysis():
    """Clear results from previous analysis commands."""
    st.session_state.pop("analysis_result", None)
    st.session_state.pop("analysis_command", None)
    st.session_state.pop("analysis_question", None)


def update_dataset(dataframe):
    """Save a cleaned dataset and clear old results."""
    st.session_state["dataframe"] = dataframe
    clear_analysis()


def format_result(result, command):
    """Format a numeric result for display."""
    operation = command.get("operation")

    if operation == "count":
        return f"{int(result):,}"

    if isinstance(result, (int, float)):
        return f"{result:,.2f}"

    return str(result)


# Page header

st.title("SWANA")
st.subheader("Smart Web Analytics & Narrative Assistant")

st.write(
    "Explore, clean, and analyze CSV or Excel datasets "
    "using natural-language commands."
)

st.divider()


# File uploader

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)


if uploaded_file is None:
    st.info(
        "Upload a CSV or Excel dataset to get started."
    )

else:
    try:
        # Identify the uploaded file
        file_id = (
            uploaded_file.name,
            uploaded_file.size,
        )

        # Load the dataset only when the file changes
        if st.session_state.get("file_id") != file_id:
            dataframe = load_dataset(uploaded_file)

            st.session_state["original_dataframe"] = (
                dataframe.copy(deep=True)
            )

            st.session_state["dataframe"] = (
                dataframe.copy(deep=True)
            )

            st.session_state["file_id"] = file_id

            clear_analysis()

        # Get the current dataset
        dataframe = st.session_state["dataframe"]

        st.success(
            f"Loaded {uploaded_file.name}"
        )

        # Show the current dataset size
        st.caption(
            f"{len(dataframe):,} rows · "
            f"{len(dataframe.columns):,} columns"
        )

        st.divider()


        # Ask SWANA

        st.header("Ask SWANA")

        st.write(
            "Ask a question about your dataset or "
            "describe a cleaning operation."
        )

        # Example questions
        with st.expander("Example commands"):
            st.write(
                "- What is the average annual salary?\n"
                "- What is the total salary for Finance?\n"
                "- How many employees work in IT?\n"
                "- What is the average salary by department?\n"
                "- Remove duplicate rows."
            )

        user_request = st.text_input(
            "What would you like SWANA to do?",
            placeholder=(
                "Example: What is the average salary by department?"
            ),
            key="user_request",
        )

        if st.button(
            "Run Command",
            type="primary",
            use_container_width=True,
        ):
            if not user_request.strip():
                st.warning(
                    "Enter a command before continuing."
                )

            elif dataframe.empty:
                st.warning(
                    "The dataset has no rows to analyze."
                )

            else:
                # Remove any previous analysis before running
                clear_analysis()

                try:
                    with st.spinner(
                        "SWANA is processing your request..."
                    ):
                        # Generate a command with Groq
                        command = generate_command(
                            user_request,
                            dataframe.columns.tolist(),
                        )

                        # Validate the generated command
                        command = parse_command(command)

                        # Execute the command
                        result = dispatch_command(
                            dataframe,
                            command,
                        )

                    # Save the question and command
                    st.session_state["analysis_question"] = (
                        user_request
                    )

                    st.session_state["analysis_command"] = (
                        command
                    )

                    # Handle cleaning commands
                    if "action" in command:
                        update_dataset(result)

                        st.session_state["last_message"] = (
                            "Dataset cleaned successfully."
                        )

                        st.rerun()

                    # Save analysis results
                    st.session_state["analysis_result"] = (
                        result
                    )

                    st.success(
                        "Analysis completed successfully."
                    )

                except CommandGenerationError as error:
                    st.warning(str(error))

                except ValueError as error:
                    st.error(str(error))

                except Exception:
                    st.error(
                        "SWANA could not complete this request. "
                        "Check your dataset and try again."
                    )

        # Show messages after cleaning or resetting
        if "last_message" in st.session_state:
            st.success(
                st.session_state.pop("last_message")
            )


        # Display analysis results

        if "analysis_result" in st.session_state:
            st.divider()

            st.header("Analysis Result")

            analysis_result = (
                st.session_state["analysis_result"]
            )

            analysis_command = (
                st.session_state["analysis_command"]
            )

            analysis_question = (
                st.session_state.get(
                    "analysis_question",
                    ""
                )
            )

            if analysis_question:
                st.caption(
                    f"Question: {analysis_question}"
                )

            # Show grouped analysis
            if isinstance(
                analysis_result,
                pd.DataFrame,
            ):
                st.dataframe(
                    analysis_result,
                    use_container_width=True,
                    hide_index=True,
                )

                # Download grouped results
                st.download_button(
                    label="Download Analysis Results",
                    data=analysis_result.to_csv(
                        index=False
                    ),
                    file_name=(
                        "swana_analysis_results.csv"
                    ),
                    mime="text/csv",
                )

                # Display grouped charts
                if "group_by" in analysis_command:
                    try:
                        chart_data = (
                            prepare_grouped_chart(
                                analysis_result,
                                analysis_command["group_by"],
                                analysis_command["operation"],
                            )
                        )

                        st.subheader(
                            "Visualization"
                        )

                        chart_type = st.selectbox(
                            "Choose a chart type",
                            [
                                "Bar Chart",
                                "Line Chart",
                                "Area Chart",
                            ],
                        )

                        if chart_type == "Bar Chart":
                            st.bar_chart(
                                chart_data,
                                use_container_width=True,
                            )

                        elif chart_type == "Line Chart":
                            st.line_chart(
                                chart_data,
                                use_container_width=True,
                            )

                        else:
                            st.area_chart(
                                chart_data,
                                use_container_width=True,
                            )

                    except ValueError as error:
                        st.warning(
                            f"Chart unavailable: {error}"
                        )

            # Display single-value results
            else:
                formatted_result = format_result(
                    analysis_result,
                    analysis_command,
                )

                operation = (
                    analysis_command["operation"]
                    .replace("_", " ")
                    .title()
                )

                st.metric(
                    label=operation,
                    value=formatted_result,
                )

            # Show how SWANA interpreted the request
            with st.expander(
                "View Generated Command"
            ):
                st.json(
                    analysis_command
                )


        st.divider()


        # Data cleaning

        st.header("Data Cleaning")

        st.write(
            "Apply cleaning operations to the "
            "current dataset."
        )

        clean_column1, clean_column2 = (
            st.columns(2)
        )

        with clean_column1:
            if st.button(
                "Remove Duplicate Rows",
                use_container_width=True,
            ):
                update_dataset(
                    remove_duplicates(dataframe)
                )

                st.session_state["last_message"] = (
                    "Duplicate rows removed."
                )

                st.rerun()

            if st.button(
                "Remove Empty Columns",
                use_container_width=True,
            ):
                update_dataset(
                    remove_empty_columns(dataframe)
                )

                st.session_state["last_message"] = (
                    "Empty columns removed."
                )

                st.rerun()

        with clean_column2:
            if st.button(
                "Remove Rows With Missing Values",
                use_container_width=True,
            ):
                update_dataset(
                    remove_missing_rows(dataframe)
                )

                st.session_state["last_message"] = (
                    "Rows with missing values removed."
                )

                st.rerun()

            if st.button(
                "Standardize Column Names",
                use_container_width=True,
            ):
                update_dataset(
                    standardize_column_names(
                        dataframe
                    )
                )

                st.session_state["last_message"] = (
                    "Column names standardized."
                )

                st.rerun()


        # Reset the dataset

        if st.button(
            "Reset Dataset",
            use_container_width=True,
        ):
            update_dataset(
                st.session_state[
                    "original_dataframe"
                ].copy(deep=True)
            )

            st.session_state["last_message"] = (
                "Dataset restored to its original state."
            )

            st.rerun()


        st.divider()


        # Analyze the current dataset

        dataframe = (
            st.session_state["dataframe"]
        )

        summary = get_dataset_summary(
            dataframe
        )

        column_information = (
            get_column_summary(
                dataframe
            )
        )

        quality_report = get_data_quality(
            dataframe
        )

        missing_by_column = (
            quality_report["missing_by_column"]
        )

        duplicate_rows = (
            quality_report["duplicate_rows"]
        )


        # Dataset overview

        st.header("Dataset Overview")

        column1, column2, column3 = (
            st.columns(3)
        )

        with column1:
            st.metric(
                "Rows",
                f"{summary['rows']:,}",
            )

        with column2:
            st.metric(
                "Columns",
                f"{summary['columns']:,}",
            )

        with column3:
            st.metric(
                "Missing Values",
                f"{summary['missing_values']:,}",
            )

        column4, column5, column6 = (
            st.columns(3)
        )

        with column4:
            st.metric(
                "Duplicate Rows",
                f"{summary['duplicate_rows']:,}",
            )

        with column5:
            st.metric(
                "Numeric Columns",
                f"{summary['numeric_columns']:,}",
            )

        with column6:
            st.metric(
                "Text Columns",
                f"{summary['text_columns']:,}",
            )


        # Data quality

        st.header("Data Quality")

        quality_column1, quality_column2 = (
            st.columns(2)
        )

        with quality_column1:
            st.subheader("Missing Values")

            if missing_by_column:
                st.warning(
                    "Missing values were detected."
                )

                missing_table = pd.DataFrame(
                    [
                        {
                            "Column": column,
                            "Missing Values": count,
                        }
                        for column, count
                        in missing_by_column.items()
                    ]
                )

                st.dataframe(
                    missing_table,
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.success(
                    "No missing values detected."
                )

        with quality_column2:
            st.subheader("Duplicate Rows")

            if duplicate_rows:
                st.warning(
                    f"{duplicate_rows:,} duplicate "
                    "row(s) detected."
                )

            else:
                st.success(
                    "No duplicate rows detected."
                )


        st.divider()


        # Dataset preview

        st.header("Data Preview")

        if len(dataframe) > 0:
            preview_rows = st.slider(
                "Number of rows to display",
                min_value=1,
                max_value=min(
                    100,
                    len(dataframe),
                ),
                value=min(
                    10,
                    len(dataframe),
                ),
            )

            st.dataframe(
                dataframe.head(
                    preview_rows
                ),
                use_container_width=True,
            )

        else:
            st.warning(
                "The dataset does not contain any rows."
            )

        # Download the working dataset
        st.download_button(
            label="Download Current Dataset",
            data=dataframe.to_csv(
                index=False
            ),
            file_name=(
                "swana_cleaned_dataset.csv"
            ),
            mime="text/csv",
        )


        st.divider()


        # Column information

        st.header("Column Information")

        st.dataframe(
            column_information,
            use_container_width=True,
            hide_index=True,
        )


        # Numeric statistics

        numeric_columns = (
            dataframe.select_dtypes(
                include="number"
            )
        )

        if (
            len(numeric_columns.columns) > 0
            and len(dataframe) > 0
        ):
            st.header("Numeric Summary")

            st.dataframe(
                numeric_columns
                .describe()
                .transpose(),
                use_container_width=True,
            )

        else:
            st.info(
                "No numeric data is available "
                "for statistical analysis."
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