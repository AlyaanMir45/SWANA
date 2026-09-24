
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
    layout="wide",
)


# Page header

st.title("SWANA")
st.subheader("Smart Web Analytics & Narrative Assistant")

st.write(
    "Upload a CSV or Excel dataset to explore its structure, "
    "clean the data, and analyze its contents."
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
        # Create an ID for the uploaded file
        file_id = (
            uploaded_file.name,
            uploaded_file.size,
        )

        # Load a new dataset only when a new file is uploaded
        if st.session_state.get("file_id") != file_id:
            dataframe = load_dataset(uploaded_file)

            st.session_state["original_dataframe"] = dataframe.copy()
            st.session_state["dataframe"] = dataframe.copy()
            st.session_state["file_id"] = file_id

            # Clear results from any previously uploaded dataset
            st.session_state.pop("analysis_result", None)
            st.session_state.pop("analysis_command", None)

        # Get the current working dataset
        dataframe = st.session_state["dataframe"]

        st.success(
            f"Successfully loaded: {uploaded_file.name}"
        )


        # Ask SWANA

        st.header("Ask SWANA")

        st.write(
            "Enter a command to clean or analyze the dataset."
        )

        user_request = st.text_input(
            "What would you like SWANA to do?"
        )

        if st.button("Run Command"):
            if not user_request.strip():
                st.warning("Enter a command first.")
                st.stop()

            try:
                # Convert the user's request into a command
                command = generate_command(
                    user_request,
                    dataframe.columns.tolist(),
                )

                # Validate the command
                command = parse_command(command)

                # Run the command
                result = dispatch_command(
                    dataframe,
                    command,
                )

                # Cleaning commands update the working dataset
                if "action" in command:
                    st.session_state["dataframe"] = result

                    # Clear previous analysis results and charts
                    st.session_state.pop(
                        "analysis_result",
                        None,
                    )
                    st.session_state.pop(
                        "analysis_command",
                        None,
                    )

                    st.success(
                        "Dataset cleaned successfully."
                    )

                    st.rerun()

                # Grouped analysis returns a table and chart
                elif "group_by" in command:
                    st.session_state["analysis_result"] = result
                    st.session_state["analysis_command"] = command

                    st.success(
                        "Grouped analysis completed successfully."
                    )

                # Regular analysis returns a single value
                else:
                    st.session_state["analysis_result"] = result

                    # Remove any previous grouped chart
                    st.session_state.pop(
                        "analysis_command",
                        None,
                    )

                    st.success(
                        "Analysis completed successfully."
                    )

            except CommandGenerationError as error:
                st.warning(str(error))

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(
                    f"Could not complete the command: {error}"
                )


        # Display the latest analysis result

        if "analysis_result" in st.session_state:
            st.subheader("Analysis Result")

            analysis_result = st.session_state["analysis_result"]

            # Display grouped analysis as a table and chart
            if isinstance(analysis_result, pd.DataFrame):
                st.dataframe(
                    analysis_result,
                    use_container_width=True,
                    hide_index=True,
                )

                # Download analysis results
                st.download_button(
                    label="Download Analysis Results",
                    data=analysis_result.to_csv(index=False),
                    file_name="swana_analysis_results.csv",
                    mime="text/csv",
                )

                # Get the command associated with this result
                analysis_command = st.session_state.get(
                    "analysis_command"
                )

                if (
                    analysis_command
                    and "group_by" in analysis_command
                ):
                    # Prepare grouped results for visualization
                    chart_data = prepare_grouped_chart(
                        analysis_result,
                        analysis_command["group_by"],
                        analysis_command["operation"],
                    )

                    st.subheader("Visualization")

                    # Choose the chart type
                    chart_type = st.selectbox(
                        "Choose a chart type",
                        [
                            "Bar Chart",
                            "Line Chart",
                            "Area Chart",
                        ],
                    )

                    # Display a bar chart
                    if chart_type == "Bar Chart":
                        st.bar_chart(
                            chart_data,
                            use_container_width=True,
                        )

                    # Display a line chart
                    elif chart_type == "Line Chart":
                        st.line_chart(
                            chart_data,
                            use_container_width=True,
                        )

                    # Display an area chart
                    else:
                        st.area_chart(
                            chart_data,
                            use_container_width=True,
                        )

            # Display ordinary analysis as a single value
            else:
                st.write(analysis_result)


        # Data cleaning

        st.header("Data Cleaning")

        st.write(
            "Apply cleaning operations to the uploaded dataset."
        )

        clean_column1, clean_column2 = st.columns(2)

        with clean_column1:
            if st.button(
                "Remove Duplicate Rows",
                use_container_width=True,
            ):
                st.session_state["dataframe"] = remove_duplicates(
                    dataframe
                )

                # Clear previous analysis results and charts
                st.session_state.pop(
                    "analysis_result",
                    None,
                )
                st.session_state.pop(
                    "analysis_command",
                    None,
                )

                st.rerun()

            if st.button(
                "Remove Empty Columns",
                use_container_width=True,
            ):
                st.session_state["dataframe"] = remove_empty_columns(
                    dataframe
                )

                # Clear previous analysis results and charts
                st.session_state.pop(
                    "analysis_result",
                    None,
                )
                st.session_state.pop(
                    "analysis_command",
                    None,
                )

                st.rerun()

        with clean_column2:
            if st.button(
                "Remove Rows With Missing Values",
                use_container_width=True,
            ):
                st.session_state["dataframe"] = remove_missing_rows(
                    dataframe
                )

                # Clear previous analysis results and charts
                st.session_state.pop(
                    "analysis_result",
                    None,
                )
                st.session_state.pop(
                    "analysis_command",
                    None,
                )

                st.rerun()

            if st.button(
                "Standardize Column Names",
                use_container_width=True,
            ):
                st.session_state["dataframe"] = standardize_column_names(
                    dataframe
                )

                # Clear previous analysis results and charts
                st.session_state.pop(
                    "analysis_result",
                    None,
                )
                st.session_state.pop(
                    "analysis_command",
                    None,
                )

                st.rerun()


        # Reset the dataset

        if st.button("Reset Dataset"):
            st.session_state["dataframe"] = (
                st.session_state["original_dataframe"].copy()
            )

            # Clear previous analysis results and charts
            st.session_state.pop(
                "analysis_result",
                None,
            )
            st.session_state.pop(
                "analysis_command",
                None,
            )

            st.rerun()


        # Analyze the current dataset

        dataframe = st.session_state["dataframe"]

        summary = get_dataset_summary(dataframe)
        column_information = get_column_summary(dataframe)
        quality_report = get_data_quality(dataframe)

        # Get data quality results
        missing_by_column = quality_report["missing_by_column"]
        duplicate_rows = quality_report["duplicate_rows"]


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
            st.warning(
                "Missing values were detected."
            )

            for column, missing_count in missing_by_column.items():
                st.write(
                    f"{column}: {missing_count} missing value(s)"
                )

        else:
            st.success(
                "No missing values were detected."
            )


        # Show duplicate row problems
        if duplicate_rows:
            st.warning(
                f"{duplicate_rows} duplicate row(s) were detected."
            )

        else:
            st.success(
                "No duplicate rows were detected."
            )


        # Dataset preview

        st.header("Data Preview")

        if len(dataframe) > 0:
            preview_rows = st.slider(
                "Number of rows to display",
                min_value=1,
                max_value=min(100, len(dataframe)),
                value=min(10, len(dataframe)),
            )

            st.dataframe(
                dataframe.head(preview_rows),
                use_container_width=True,
            )

        else:
            st.warning(
                "The dataset does not contain any rows."
            )


        # Download the current working dataset

        st.download_button(
            label="Download Cleaned Dataset",
            data=dataframe.to_csv(index=False),
            file_name="swana_cleaned_dataset.csv",
            mime="text/csv",
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

        if (
            len(numeric_columns.columns) > 0
            and len(dataframe) > 0
        ):
            st.header("Numeric Summary")

            st.dataframe(
                numeric_columns.describe().transpose(),
                use_container_width=True,
            )

        else:
            st.info(
                "No numeric data is available for statistical analysis."
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