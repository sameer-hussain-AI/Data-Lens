
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Data Lens",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def load_dataset(file):

    try:
        if file.name.lower().endswith(".csv"):
            return pd.read_csv(file)

        elif file.name.lower().endswith(".xlsx"):
            return pd.read_excel(file)

    except Exception as e:
        st.error(f"Unable to read dataset: {e}")
        return None

    return None


def get_excel_download(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")

    return output.getvalue()


def display_download(df, file_format):

    if file_format == "csv":

        data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Cleaned CSV",
            data=data,
            file_name="Cleaned_Data.csv",
            mime="text/csv"
        )

    else:

        data = get_excel_download(df)

        st.download_button(
            label="Download Cleaned Excel",
            data=data,
            file_name="Cleaned_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def get_format(file):

    if file.name.lower().endswith(".csv"):
        return "csv"

    return "xlsx"


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.title("Data Lens")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Overview",
            "Data Preview",
            "Data Quality",
            "Data Cleaning",
            "Visualization",
            "Export"
        ],
        label_visibility="collapsed"
    )


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    col1, col2 = st.columns([1, 3])

    with col1:

        logo_path = Path("DataLens Analytics Logo.png")

        if logo_path.exists():
            st.image(str(logo_path), width=150)
        else:
            st.write("📊")

    with col2:

        st.title("Data Lens")
        st.subheader("Your Personal Data Analysis Workspace")

        st.write("Turn raw data into meaningful insights.")

    st.divider()

    st.header("Welcome to Data Lens!")

    st.write(
        "Analyze your datasets, improve data quality, "
        "clean missing values and discover insights "
        "through interactive visualizations."
    )

    st.divider()

    st.header("Explore Our Features")

    st.write("Everything you need for basic data analysis.")

    col1, col2 = st.columns(2, gap="large")

    with col1:

        with st.container(border=True):

            st.metric("📂 Upload Data", "CSV / Excel")
            st.caption("Import your datasets easily.")

        with st.container(border=True):

            st.metric("🧹 Clean Data", "Data Cleaning")
            st.caption("Handle missing values and duplicates.")

        with st.container(border=True):

            st.metric("📊 Visualization", "4 Chart Types")
            st.caption(
                "Create bar, line, scatter and histogram charts."
            )

    with col2:

        with st.container(border=True):

            st.metric("🔍 Explore Data", "Data Preview")
            st.caption("Explore rows, columns and records.")

        with st.container(border=True):

            st.metric("🛡️ Data Quality", "Quality Analysis")
            st.caption("Check missing values and dataset quality.")

        with st.container(border=True):

            st.metric("📥 Export Data", "PDF Reports")
            st.caption("Generate reports of your data analysis.")

    st.divider()

    st.header("About the Developer")

    with st.container(border=True):

        st.subheader("Sameer Hussain")

        st.write(
            "Aspiring Data Analyst | Python | Pandas | Streamlit"
        )

        st.write(
            "I created Data Lens to make data analysis "
            "simple, accessible and efficient. My goal is "
            "to help users understand and explore their data."
        )

    st.divider()

    st.markdown(
        """
        <div style='text-align:center; color:gray;'>
        Data Lens | Built with Python, Pandas & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

elif page == "Overview":

    st.header("Overview")

    file = st.file_uploader(
        "Start with your dataset",
        type=["csv", "xlsx"],
        key="overview_upload"
    )

    st.divider()

    if file:

        df = load_dataset(file)

        if df is not None:

            st.subheader("Dataset Preview")

            st.dataframe(df.head(5), use_container_width=True)

            st.divider()

            st.title("Dataset Statistics")

            c1, c2 = st.columns(2)

            with c1:

                with st.container(border=True):
                    st.metric("Number of Rows", df.shape[0])

                with st.container(border=True):
                    st.metric("Total Elements", df.size)

                with st.container(border=True):
                    st.metric(
                        "Duplicate Records",
                        df.duplicated().sum()
                    )

            with c2:

                with st.container(border=True):
                    st.metric("Number of Columns", df.shape[1])

                with st.container(border=True):
                    st.metric(
                        "Missing Values",
                        df.isnull().sum().sum()
                    )

            st.divider()

            st.write("**File Name:**", file.name)

            st.write(
                "**Data Format:**",
                get_format(file).upper()
            )


# --------------------------------------------------
# DATA PREVIEW PAGE
# --------------------------------------------------

elif page == "Data Preview":

    st.header("Data Preview")

    file = st.file_uploader(
        "Start with your dataset",
        type=["csv", "xlsx"],
        key="preview_upload"
    )

    st.divider()

    if file:

        df = load_dataset(file)

        if df is not None:

            c1, c2 = st.columns([1, 4])

            with c1:

                rows = st.selectbox(
                    "Rows to display",
                    [10, 20, 50, 100, 200]
                )

            with c2:

                columns = st.multiselect(
                    "Selected Columns",
                    df.columns.tolist(),
                    default=df.columns.tolist()
                )

            if columns:

                st.dataframe(
                    df[columns].head(rows),
                    use_container_width=True
                )

            else:

                st.info("No column selected.")

            st.divider()

            st.subheader("Search Records")

            search = st.text_input(
                "Search your dataset",
                placeholder="Enter a value to search..."
            )

            if search:

                mask = (
                    df.astype(str)
                    .apply(
                        lambda col: col.str.contains(
                            search,
                            case=False,
                            na=False,
                            regex=False
                        )
                    )
                    .any(axis=1)
                )

                filtered_df = df[mask]

                if not filtered_df.empty:

                    st.success(
                        f"{len(filtered_df)} matching records found."
                    )

                    st.dataframe(
                        filtered_df,
                        use_container_width=True
                    )

                else:

                    st.info("No record found.")


# --------------------------------------------------
# DATA QUALITY PAGE
# --------------------------------------------------

elif page == "Data Quality":

    st.header("Data Quality")

    file = st.file_uploader(
        "Start with your dataset",
        type=["csv", "xlsx"],
        key="quality_upload"
    )

    st.divider()

    if file:

        df = load_dataset(file)

        if df is not None:

            st.header("Data Quality Analysis")

            total_cells = df.size

            missing = df.isnull().sum().sum()

            if total_cells > 0:
                score = ((total_cells - missing) / total_cells) * 100
            else:
                score = 0

            if score >= 90:
                status = "Good Quality"

            elif score >= 70:
                status = "Average Quality"

            else:
                status = "Poor Quality"

            st.subheader("Overall Completeness Score")

            st.metric(
                "Completeness",
                f"{score:.1f}%"
            )

            st.progress(score / 100)

            if status == "Good Quality":
                st.success(status)

            elif status == "Average Quality":
                st.warning(status)

            else:
                st.error(status)

            st.divider()

            c1, c2, c3 = st.columns(3)

            with c1:

                with st.container(border=True):
                    st.metric("Missing Values", missing)

            with c2:

                with st.container(border=True):
                    st.metric(
                        "Duplicate Rows",
                        df.duplicated().sum()
                    )

            with c3:

                with st.container(border=True):
                    st.metric("Total Records", df.shape[0])

            st.divider()

            st.subheader("Missing Values By Column")

            missing_by_column = df.isnull().sum()

            with st.container(border=True):

                if missing > 0:

                    st.bar_chart(
                        missing_by_column[missing_by_column > 0],
                        horizontal=True,
                        color="#16A36A",
                        height=350
                    )

                else:

                    st.info("No Missing Values Found!")

            st.divider()

            st.subheader("Duplicated Values By Column")

            duplicate_data = pd.DataFrame({
                "Column": df.columns,
                "Duplicate Values": [
                    df[col].duplicated().sum()
                    for col in df.columns
                ]
            })

            st.dataframe(
                duplicate_data,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("Data Types")

            dtype_data = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values
            })

            st.dataframe(
                dtype_data,
                use_container_width=True,
                hide_index=True
            )


# --------------------------------------------------
# DATA CLEANING PAGE
# --------------------------------------------------

elif page == "Data Cleaning":

    st.header("Data Cleaning")

    file = st.file_uploader(
        "Start with your dataset",
        type=["csv", "xlsx"],
        key="cleaning_upload"
    )

    st.divider()

    if file:

        df = load_dataset(file)

        if df is not None:

            file_format = get_format(file)

            cleaned_df = df.copy()

            # --------------------------------------
            # HANDLE MISSING VALUES
            # --------------------------------------

            st.subheader("Handle Missing Values")

            c1, c2 = st.columns([1, 3])

            with c1:

                option = st.selectbox(
                    "Choose a method",
                    [
                        "Drop Missing Values",
                        "Fill with mean",
                        "Fill with median",
                        "Fill with mode"
                    ]
                )

            if option == "Drop Missing Values":

                available_columns = df.columns.tolist()

            elif option in ["Fill with mean", "Fill with median"]:

                available_columns = df.select_dtypes(
                    include="number"
                ).columns.tolist()

            else:

                available_columns = df.columns.tolist()

            with c2:

                column = st.multiselect(
                    "Choose columns",
                    available_columns
                )

            if st.button("Apply Cleaning", key="apply_missing"):

                if not column:

                    st.warning("Please select at least one column.")

                elif option == "Drop Missing Values":

                    cleaned_df = cleaned_df.dropna(subset=column)

                    st.success("Missing values removed successfully!")

                    display_download(cleaned_df, file_format)

                elif option == "Fill with mean":

                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mean()
                    )

                    st.success("Missing values filled with mean!")

                    display_download(cleaned_df, file_format)

                elif option == "Fill with median":

                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].median()
                    )

                    st.success("Missing values filled with median!")

                    display_download(cleaned_df, file_format)

                elif option == "Fill with mode":

                    for col in column:

                        mode_values = cleaned_df[col].mode(dropna=True)

                        if not mode_values.empty:

                            cleaned_df[col] = cleaned_df[col].fillna(
                                mode_values.iloc[0]
                            )

                    st.success("Missing values filled with mode!")

                    display_download(cleaned_df, file_format)

            st.divider()

            # --------------------------------------
            # REMOVE DUPLICATE ROWS
            # --------------------------------------

            st.subheader("Drop Duplicate Rows")

            st.write(
                "Remove duplicate records from your dataset."
            )

            st.metric(
                "Duplicate rows detected",
                df.duplicated().sum()
            )

            duplicate_opt = st.selectbox(
                "Choose how to handle duplicates",
                [
                    "Keep first",
                    "Keep last",
                    "Remove all"
                ]
            )

            if st.button("Apply Deletion", key="apply_duplicates"):

                if duplicate_opt == "Keep first":

                    cleaned_df = df.drop_duplicates(keep="first")

                elif duplicate_opt == "Keep last":

                    cleaned_df = df.drop_duplicates(keep="last")

                else:

                    cleaned_df = df.drop_duplicates(keep=False)

                st.success("Duplicate records handled successfully!")

                display_download(cleaned_df, file_format)

            st.divider()

            st.subheader("Original Dataset")

            st.dataframe(
                df.head(5),
                use_container_width=True
            )


# --------------------------------------------------
# VISUALIZATION PAGE
# --------------------------------------------------

elif page == "Visualization":

    st.header("Data Visualization")

    file = st.file_uploader(
        "Start with your dataset",
        type=["csv", "xlsx"],
        key="visualization_upload"
    )

    st.divider()

    st.subheader("Create Your Visualization")

    st.caption(
        "Create charts and discover patterns in your dataset."
    )

    if file:

        df = load_dataset(file)

        if df is not None:

            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_columns = df.select_dtypes(
                include=["object", "category", "string"]
            ).columns.tolist()

            chart = st.selectbox(
                "Select Chart Type",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Histogram"
                ]
            )

            x_axis = None
            y_axis = None

            # ----------------------------------
            # BAR CHART
            # ----------------------------------

            if chart == "Bar Chart":

                if not categorical_columns:

                    st.warning(
                        "Bar chart requires at least one categorical column."
                    )

                elif not numeric_columns:

                    st.warning(
                        "Bar chart requires at least one numerical column."
                    )

                else:

                    c1, c2 = st.columns(2)

                    with c1:

                        x_axis = st.selectbox(
                            "Select Column For X-Axis",
                            categorical_columns,
                            key="bar_x"
                        )

                    with c2:

                        y_axis = st.selectbox(
                            "Select Column For Y-Axis",
                            numeric_columns,
                            key="bar_y"
                        )

            # ----------------------------------
            # LINE CHART
            # ----------------------------------

            elif chart == "Line Chart":

                if not numeric_columns:

                    st.warning(
                        "Line chart requires at least one numerical column."
                    )

                else:

                    c1, c2 = st.columns(2)

                    with c1:

                        x_axis = st.selectbox(
                            "Select Column For X-Axis",
                            df.columns.tolist(),
                            key="line_x"
                        )

                    with c2:

                        y_axis = st.selectbox(
                            "Select Column For Y-Axis",
                            numeric_columns,
                            key="line_y"
                        )

            # ----------------------------------
            # SCATTER PLOT
            # ----------------------------------

            elif chart == "Scatter Plot":

                if len(numeric_columns) < 2:

                    st.warning(
                        "Scatter plot requires at least two numerical columns."
                    )

                else:

                    c1, c2 = st.columns(2)

                    with c1:

                        x_axis = st.selectbox(
                            "Select Column For X-Axis",
                            numeric_columns,
                            key="scatter_x")