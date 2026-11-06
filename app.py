import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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

def load_dataset(uploaded_file):
    """Read CSV/XLSX safely without depending on the file cursor position."""
    try:
        file_bytes = uploaded_file.getvalue()

        if uploaded_file.name.lower().endswith(".csv"):
            try:
                return pd.read_csv(BytesIO(file_bytes))
            except UnicodeDecodeError:
                return pd.read_csv(BytesIO(file_bytes), encoding="latin-1")

        if uploaded_file.name.lower().endswith(".xlsx"):
            return pd.read_excel(BytesIO(file_bytes), engine="openpyxl")

        st.error("Please upload a CSV or XLSX file.")

    except Exception as error:
        st.error(f"Unable to read dataset: {error}")

    return None


def get_excel_download(dataframe):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Cleaned Data")

    output.seek(0)
    return output.getvalue()


def get_pdf_report(dataframe, filename):
    """Create a compact PDF report with summary and column-level details."""
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    page_width, page_height = A4
    y = page_height - 50

    pdf.setTitle("Data Lens Analysis Report")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(42, y, "Data Lens - Analysis Report")
    y -= 28

    pdf.setFont("Helvetica", 10)
    pdf.drawString(42, y, f"File: {filename}")
    y -= 16
    pdf.drawString(42, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 28

    total_cells = dataframe.size
    missing = int(dataframe.isna().sum().sum())
    completeness = ((total_cells - missing) / total_cells * 100) if total_cells else 100

    summary = [
        f"Rows: {dataframe.shape[0]}",
        f"Columns: {dataframe.shape[1]}",
        f"Total cells: {total_cells}",
        f"Missing values: {missing}",
        f"Duplicate rows: {int(dataframe.duplicated().sum())}",
        f"Completeness: {completeness:.1f}%"
    ]

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(42, y, "Dataset Summary")
    y -= 20
    pdf.setFont("Helvetica", 10)

    for item in summary:
        pdf.drawString(48, y, item)
        y -= 16

    y -= 12
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(42, y, "Column Details")
    y -= 20

    def draw_table_header():
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(45, y, "Column")
        pdf.drawString(275, y, "Data Type")
        pdf.drawString(405, y, "Missing")
        pdf.setFont("Helvetica", 8)

    draw_table_header()

    for column in dataframe.columns:
        if y < 55:
            pdf.showPage()
            y = page_height - 50
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(42, y, "Column Details (continued)")
            y -= 25
            draw_table_header()

        safe_name = str(column).encode("latin-1", "replace").decode("latin-1")[:38]
        safe_dtype = str(dataframe[column].dtype)[:18]
        missing_count = str(int(dataframe[column].isna().sum()))

        pdf.drawString(45, y, safe_name)
        pdf.drawString(275, y, safe_dtype)
        pdf.drawString(405, y, missing_count)
        y -= 14

    pdf.save()
    output.seek(0)
    return output.getvalue()


def show_dataframe(dataframe):
    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )


def apply_missing_value_method(dataframe, method, selected_columns):
    result = dataframe.copy()

    if method == "Drop Missing Values":
        return result.dropna(subset=selected_columns)

    for column in selected_columns:
        if method == "Fill with mean":
            if pd.api.types.is_numeric_dtype(result[column]):
                result[column] = result[column].fillna(result[column].mean())

        elif method == "Fill with median":
            if pd.api.types.is_numeric_dtype(result[column]):
                result[column] = result[column].fillna(result[column].median())

        elif method == "Fill with mode":
            modes = result[column].mode(dropna=True)
            if not modes.empty:
                result[column] = result[column].fillna(modes.iloc[0])

    return result


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "original_df" not in st.session_state:
    st.session_state.original_df = None

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "dataset_signature" not in st.session_state:
    st.session_state.dataset_signature = None

if "source_filename" not in st.session_state:
    st.session_state.source_filename = "dataset"


# --------------------------------------------------
# SIDEBAR NAVIGATION AND SHARED UPLOAD
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

    st.divider()
    st.subheader("Your Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"],
        key="main_dataset_upload"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        signature = (
            uploaded_file.name,
            len(file_bytes),
            hash(file_bytes)
        )

        if signature != st.session_state.dataset_signature:
            loaded_df = load_dataset(uploaded_file)

            if loaded_df is not None:
                st.session_state.original_df = loaded_df.copy()
                st.session_state.cleaned_df = loaded_df.copy()
                st.session_state.dataset_signature = signature
                st.session_state.source_filename = uploaded_file.name
                st.success("Dataset uploaded successfully.")

    if st.session_state.cleaned_df is not None:
        st.caption(f"Loaded: {st.session_state.source_filename}")
        if st.button("Remove current dataset", use_container_width=True):
            st.session_state.original_df = None
            st.session_state.cleaned_df = None
            st.session_state.dataset_signature = None
            st.session_state.source_filename = "dataset"
            st.rerun()


# Use the working dataset across every section.
original_df = st.session_state.original_df
df = st.session_state.cleaned_df
has_data = df is not None


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
        "Analyze your datasets, improve data quality, clean missing values "
        "and discover insights through interactive visualizations."
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
            st.caption("Create bar, line, scatter and histogram charts.")

    with col2:
        with st.container(border=True):
            st.metric("🔍 Explore Data", "Data Preview")
            st.caption("Explore rows, columns and records.")

        with st.container(border=True):
            st.metric("🛡️ Data Quality", "Quality Analysis")
            st.caption("Check missing values and dataset quality.")

        with st.container(border=True):
            st.metric("📥 Export Data", "CSV / Excel / PDF")
            st.caption("Download your cleaned dataset and PDF report.")

    st.divider()
    st.header("About the Developer")

    with st.container(border=True):
        st.subheader("Sameer Hussain")
        st.write("Aspiring Data Analyst | Python | Pandas | Streamlit")
        st.write(
            "I created Data Lens to make data analysis simple, accessible "
            "and efficient. My goal is to help users understand and explore their data."
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

    if not has_data:
        st.info("Upload a CSV or XLSX file using the sidebar.")
    else:
        st.caption(f"File: {st.session_state.source_filename}")
        st.subheader("Dataset Preview")
        show_dataframe(df.head(5))

        st.divider()
        st.subheader("Dataset Statistics")

        c1, c2, c3 = st.columns(3)
        c1.metric("Number of Rows", f"{df.shape[0]:,}")
        c2.metric("Number of Columns", f"{df.shape[1]:,}")
        c3.metric("Total Elements", f"{df.size:,}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
        c2.metric("Duplicate Records", f"{int(df.duplicated().sum()):,}")
        c3.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

        st.divider()
        st.subheader("Column Information")

        info = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isna().sum().values,
            "Unique Values": df.nunique(dropna=True).values
        })
        show_dataframe(info)


# --------------------------------------------------
# DATA PREVIEW PAGE
# --------------------------------------------------

elif page == "Data Preview":

    st.header("Data Preview")

    if not has_data:
        st.info("Upload a dataset using the sidebar.")
    else:
        c1, c2 = st.columns([1, 4])

        with c1:
            rows = st.selectbox("Rows to display", [10, 20, 50, 100, 200])

        with c2:
            columns = st.multiselect(
                "Selected Columns",
                df.columns.tolist(),
                default=df.columns.tolist(),
                key="preview_columns"
            )

        if columns:
            show_dataframe(df[columns].head(rows))
        else:
            st.info("Select at least one column.")

        st.divider()
        st.subheader("Search Records")

        search = st.text_input(
            "Search your dataset",
            placeholder="Enter a value to search..."
        )

        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False,
                    regex=False
                )
            ).any(axis=1)

            filtered_df = df.loc[mask]

            if not filtered_df.empty:
                st.success(f"{len(filtered_df):,} matching records found.")
                show_dataframe(filtered_df)
            else:
                st.info("No records found.")


# --------------------------------------------------
# DATA QUALITY PAGE
# --------------------------------------------------

elif page == "Data Quality":

    st.header("Data Quality")

    if not has_data:
        st.info("Upload a dataset using the sidebar.")
    else:
        total_cells = df.size
        missing = int(df.isna().sum().sum())
        score = ((total_cells - missing) / total_cells * 100) if total_cells else 100

        st.subheader("Overall Completeness Score")
        st.metric("Completeness", f"{score:.1f}%")
        st.progress(score / 100)

        if score >= 90:
            st.success("Good Quality")
        elif score >= 70:
            st.warning("Average Quality")
        else:
            st.error("Poor Quality")

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Missing Values", f"{missing:,}")
        c2.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
        c3.metric("Total Records", f"{df.shape[0]:,}")

        st.divider()
        st.subheader("Missing Values By Column")

        missing_by_column = df.isna().sum()
        missing_by_column = missing_by_column[missing_by_column > 0]

        with st.container(border=True):
            if not missing_by_column.empty:
                st.bar_chart(
                    missing_by_column,
                    horizontal=True,
                    color="#16A36A",
                    height=350
                )
            else:
                st.success("No Missing Values Found!")

        st.divider()
        st.subheader("Duplicated Values By Column")

        duplicate_data = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Duplicate Values": [
                int(df[column].duplicated().sum())
                for column in df.columns
            ]
        })
        show_dataframe(duplicate_data)

        st.divider()
        st.subheader("Data Types")

        dtype_data = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values
        })
        show_dataframe(dtype_data)


# --------------------------------------------------
# DATA CLEANING PAGE
# --------------------------------------------------

elif page == "Data Cleaning":

    st.header("Data Cleaning")

    if not has_data:
        st.info("Upload a dataset using the sidebar.")
    else:
        st.caption("Changes are retained as you move between Data Lens sections.")

        st.subheader("Handle Missing Values")

        option = st.selectbox(
            "Choose a method",
            [
                "Drop Missing Values",
                "Fill with mean",
                "Fill with median",
                "Fill with mode"
            ],
            key="cleaning_method"
        )

        if option in ["Fill with mean", "Fill with median"]:
            available_columns = df.select_dtypes(include="number").columns.tolist()
        else:
            available_columns = df.columns.tolist()

        selected_columns = st.multiselect(
            "Choose columns",
            available_columns,
            key="cleaning_columns"
        )

        if st.button("Apply Cleaning", key="apply_missing", type="primary"):
            if not selected_columns:
                st.warning("Please select at least one column.")
            else:
                updated_df = apply_missing_value_method(
                    df,
                    option,
                    selected_columns
                )
                st.session_state.cleaned_df = updated_df
                st.success("Cleaning operation applied successfully.")
                st.rerun()

        st.divider()
        st.subheader("Drop Duplicate Rows")
        st.metric("Duplicate rows detected", f"{int(df.duplicated().sum()):,}")

        duplicate_option = st.selectbox(
            "Choose how to handle duplicates",
            ["Keep first", "Keep last", "Remove all"],
            key="duplicate_option"
        )

        if st.button("Apply Duplicate Removal", key="apply_duplicates"):
            keep_value = {
                "Keep first": "first",
                "Keep last": "last",
                "Remove all": False
            }[duplicate_option]

            st.session_state.cleaned_df = df.drop_duplicates(keep=keep_value)
            st.success("Duplicate operation applied successfully.")
            st.rerun()

        st.divider()
        st.subheader("Current Working Dataset")
        show_dataframe(df.head(10))

        if st.button("Reset to Original Dataset"):
            st.session_state.cleaned_df = original_df.copy()
            st.success("Dataset restored to its original state.")
            st.rerun()


# --------------------------------------------------
# VISUALIZATION PAGE
# --------------------------------------------------

elif page == "Visualization":

    st.header("Data Visualization")
    st.caption("Choose a chart type and columns, then click Generate Chart.")

    if not has_data:
        st.info("Upload a dataset using the sidebar.")
    else:
        numeric_columns = df.select_dtypes(include="number").columns.tolist()
        all_columns = df.columns.tolist()

        chart = st.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"],
            key="chart_type"
        )

        x_axis = None
        y_axis = None
        valid_chart = True

        if chart == "Bar Chart":
            if not numeric_columns:
                st.warning("Bar chart requires at least one numerical column.")
                valid_chart = False
            else:
                c1, c2 = st.columns(2)

                with c1:
                    x_axis = st.selectbox(
                        "Select Category / X-Axis",
                        all_columns,
                        key="bar_x"
                    )

                with c2:
                    y_axis = st.selectbox(
                        "Select Numerical / Y-Axis",
                        numeric_columns,
                        key="bar_y"
                    )

                aggregation = st.selectbox(
                    "Aggregation",
                    ["Sum", "Mean", "Count"],
                    key="bar_aggregation"
                )

        elif chart == "Line Chart":
            if not numeric_columns:
                st.warning("Line chart requires at least one numerical column.")
                valid_chart = False
            else:
                c1, c2 = st.columns(2)

                with c1:
                    x_axis = st.selectbox(
                        "Select X-Axis",
                        all_columns,
                        key="line_x"
                    )

                with c2:
                    y_axis = st.selectbox(
                        "Select Y-Axis",
                        numeric_columns,
                        key="line_y"
                    )

        elif chart == "Scatter Plot":
            if len(numeric_columns) < 2:
                st.warning("Scatter plot requires at least two numerical columns.")
                valid_chart = False
            else:
                c1, c2 = st.columns(2)

                with c1:
                    x_axis = st.selectbox(
                        "Select X-Axis",
                        numeric_columns,
                        key="scatter_x"
                    )

                with c2:
                    y_options = [column for column in numeric_columns if column != x_axis]
                    y_axis = st.selectbox(
                        "Select Y-Axis",
                        y_options,
                        key="scatter_y"
                    )

        else:
            if not numeric_columns:
                st.warning("Histogram requires at least one numerical column.")
                valid_chart = False
            else:
                x_axis = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns,
                    key="histogram_column"
                )
                bins = st.slider(
                    "Number of bins",
                    min_value=5,
                    max_value=60,
                    value=20,
                    key="histogram_bins"
                )

        st.divider()

        if valid_chart and st.button(
            "Generate Chart",
            type="primary",
            use_container_width=True,
            key="generate_chart"
        ):
            try:
                fig, ax = plt.subplots(figsize=(10, 5))

                if chart == "Bar Chart":
                    grouped = df.groupby(x_axis, dropna=False)[y_axis]

                    if aggregation == "Sum":
                        plot_data = grouped.sum()
                    elif aggregation == "Mean":
                        plot_data = grouped.mean()
                    else:
                        plot_data = grouped.count()

                    plot_data = plot_data.sort_values(ascending=False).head(50)
                    plot_data.plot(kind="bar", ax=ax)
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(f"{aggregation} of {y_axis}")

                elif chart == "Line Chart":
                    plot_data = df[[x_axis, y_axis]].dropna()

                    if pd.api.types.is_datetime64_any_dtype(plot_data[x_axis]):
                        plot_data = plot_data.sort_values(x_axis)

                    ax.plot(
                        plot_data[x_axis].astype(str),
                        plot_data[y_axis],
                        marker="o",
                        linewidth=1.5
                    )
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)

                    if len(plot_data) > 30:
                        ax.tick_params(axis="x", rotation=45)

                elif chart == "Scatter Plot":
                    plot_data = df[[x_axis, y_axis]].dropna()
                    ax.scatter(plot_data[x_axis], plot_data[y_axis], alpha=0.65)
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)

                else:
                    values = pd.to_numeric(df[x_axis], errors="coerce").dropna()
                    ax.hist(values, bins=bins, edgecolor="black")
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel("Frequency")

                ax.set_title(chart)
                ax.grid(axis="y", alpha=0.25)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            except Exception as error:
                st.error(f"Unable to generate chart: {error}")


# --------------------------------------------------
# EXPORT PAGE
# --------------------------------------------------

elif page == "Export":

    st.header("Export")
    st.write("Download your current working dataset and its analysis report.")

    if not has_data:
        st.info("Upload a dataset using the sidebar.")
    else:
        st.subheader("Dataset Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", f"{df.shape[1]:,}")
        c3.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")

        st.divider()
        st.subheader("Download Dataset")

        c1, c2 = st.columns(2)

        with c1:
            st.download_button(
                label="Download Cleaned CSV",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="Data_Lens_Cleaned_Data.csv",
                mime="text/csv",
                use_container_width=True
            )

        with c2:
            st.download_button(
                label="Download Cleaned Excel",
                data=get_excel_download(df),
                file_name="Data_Lens_Cleaned_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.divider()
        st.subheader("Download Analysis Report")

        st.download_button(
            label="Download PDF Report",
            data=get_pdf_report(df, st.session_state.source_filename),
            file_name="Data_Lens_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.caption(
            "The PDF report includes dataset size, completeness, duplicate rows "
            "and column-level missing-value details."
        )
