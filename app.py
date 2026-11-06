I'llimport streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt


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
            "Export",
        ],
        label_visibility="collapsed",
    )
if page == "Home":
    # Header
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("DataLens Analytics Logo.png", width=150)

    with col2:
        st.title("Data Lens")
        st.subheader("Your Personal Data Analysis Workspace")
        st.write("Turn raw data into meaningful insights.")

    st.divider()

    # Welcome section
    st.header("Welcome to Data Lens!")

    st.write(
        "Analyze your datasets, improve data quality, "
        "clean missing values and discover insights "
        "through interactive visualizations."
    )

    st.divider()

    # Features
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
            st.metric("📥 Export Data", "PDF Reports")
            st.caption("Generate reports of your data analysis.")

    st.divider()

    # About Developer
    st.header("About the Developer")

    with st.container(border=True):
        st.subheader("Sameer Hussain")
        st.write("Aspiring Data Analyst | Python | Pandas | Streamlit")

        st.write(
            "I created Data Lens to make data analysis "
            "simple, accessible and efficient. My goal is "
            "to help users understand and explore their data."
        )

    st.divider()

    # Footer
    st.markdown(
        "<div style='text-align:center; color:gray;'>"
        "Data Lens | Built with Python, Pandas & Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


elif page == "Overview":
    st.header("Overview")
    file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
    st.divider()
    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
            st.dataframe(df.head(5))
            st.divider()
            st.title("Dataset Statistics")
            c1, c2 = st.columns([1, 3])
            st.divider()
            with c1:
                with st.container(border=True):
                    st.metric("Number of Rows", df.shape[0])
            with c2:
                with st.container(border=True):
                    st.metric("Number of Columns", df.shape[1])
            with c1:
                with st.container(border=True):
                    st.metric("Total Elements", df.shape[0] * df.shape[1])
            with c2:
                with st.container(border=True):
                    st.metric("Number of missing values", df.isnull().sum().sum())
            with c1:
                with st.container(border=True):
                    st.metric("Duplicate Records", df.duplicated().sum().sum())
            st.write("File Name: ", file.name)
            st.write("Data Format: ", "CSV")
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
            st.dataframe(df.head(5))
            st.divider()
            c1, c2 = st.columns([1, 3])
            with c1:
                with st.container(border=True):
                    st.metric("Number of Rows", df.shape[0])
            with c2:
                with st.container(border=True):
                    st.metric("Number of Columns", df.shape[1])
            with c1:
                with st.container(border=True):
                    st.metric("Total Elements", df.shape[0] * df.shape[1])
            with c2:
                with st.container(border=True):
                    st.metric("Number of missing values", df.isnull().sum().sum())
            with c1:
                with st.container(border=True):
                    st.metric("Duplicate Records", df.duplicated().sum().sum())
            st.write("File Name: ", file.name)
            st.write("Data Format: ", "Excel")
        else:
            st.error("File type not supported")

elif page == "Data Preview":
    st.header("Data Preview")
    file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
    st.divider()
    if file:

        if file.name.endswith(".csv"):
            c1, c2 = st.columns([1, 4])
            df = pd.read_csv(file)
            with c1:
                rows = st.selectbox("Rows to display", [10, 20, 50, 100, 200])
            with c2:
                columns = st.multiselect("Selected Columns", df.columns)
            if columns:
                st.dataframe(df[columns].head(rows))
            else:
                st.info("No Column Selected")
            search = st.text_input("Search Records", type="search")

            if search:
                mask = (
                    df.astype(str)
                    .apply(lambda col: col.str.contains(search, case=False, na=False))
                    .any(axis=1)
                )

                filtered_df = df[mask]

                if not filtered_df.empty:
                    st.dataframe(filtered_df)
                else:
                    st.info("No record found")

        elif file.name.endswith(".xlsx"):
            c1, c2 = st.columns([1, 4])
            df = pd.read_excel(file)
            with c1:
                rows = st.selectbox("Rows to display", [10, 20, 50, 100, 200])
            with c2:
                columns = st.multiselect("Selected Columns", df.columns)
            if columns:
                st.dataframe(df[columns].head(rows))
            else:
                st.info("No Column Selected")
            search = st.text_input("Search Records")

            if search:
                mask = (
                    df.astype(str)
                    .apply(lambda col: col.str.contains(search, case=False, na=False))
                    .any(axis=1)
                )

                filtered_df = df[mask]

                if not filtered_df.empty:
                    st.dataframe(filtered_df)
                else:
                    st.info("No record found")
        else:
            st.error("File type not supported")
elif page == "Data Quality":
    st.header("Data Quality")
    file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
    st.divider()
    st.header("Data Quality Analysis")
    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

            score = ((df.size - df.isnull().sum().sum()) / df.size) * 100
            if score >= 90:
                status = "Good Quality"
            elif score >= 70:
                status = "Average Quality"
            else:
                status = "Poor Quality"
            st.subheader("Overall Completness Score")
            st.metric("Completeness", f"{score:.1f}%")
            st.progress(score / 100)
            if status == "Good Quality":
                st.success(status)
            elif status == "Average Quality":
                st.warning(status)
            else:
                st.error(status)
            c1, c2, c3 = st.columns(3)
            with c1:
                with st.container(border=True):
                    st.metric("Missing Values", df.isnull().sum().sum())
            with c2:
                with st.container(border=True):
                    st.metric("Duplicate Rows", df.duplicated().sum())
            with c3:
                with st.container(border=True):
                    st.metric("Total Records", df.size)
            st.subheader("Missing Values By Column")
            with st.container(border=True):
                if df.isnull().sum().sum() > 0:

                    st.bar_chart(
                        data=df.isnull().sum(),
                        horizontal="True",
                        color="#16A36A",
                        height=350,
                    )
                else:
                    st.info("No Missing Values")

            columns = df.columns
            st.subheader("Duplicated Values By Column")
            for i in columns:
                st.write(i, df[i].duplicated().sum())

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

            score = ((df.size - df.isnull().sum().sum()) / df.size) * 100
            if score >= 90:
                status = "Good Quality"
            elif score >= 70:
                status = "Average Quality"
            else:
                status = "Poor Quality"
            st.subheader("Overall Completness Score")
            st.metric("Completeness", f"{score:.1f}%")
            st.progress(score / 100)
            if status == "Good Quality":
                st.success(status)
            elif status == "Average Quality":
                st.warning(status)
            else:
                st.error(status)
            c1, c2, c3 = st.columns(3)
            with c1:
                with st.container(border=True):
                    st.metric("Missing Values", df.isnull().sum().sum())
                with c2:
                    with st.container(border=True):
                        st.metric("Duplicate Rows", df.duplicated().sum())
                with c3:
                    with st.container(border=True):
                        st.metric("Total Records", df.size)
            st.subheader("Missing Values By Column")
            with st.container(border=True):
                if df.isnull().sum().sum() > 0:
                    st.bar_chart(
                        data=df.isnull().sum(),
                        horizontal="True",
                        color="#16A36A",
                        height=350,
                    )
                else:
                    st.info("No Missing Values")
            columns = df.columns
            st.subheader("Duplicated Values By Column")
            for i in columns:
                st.write(i, df[i].duplicated().sum())
        else:
            st.error("File type not supported")
elif page == "Data Cleaning":
    st.header("Data Cleaning")
    file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
    st.divider()
    st.subheader("Handle Missing Values")
    c1, c2 = st.columns([1, 3])
    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
            cleaned_df = df.copy()
            with c1:
                option = st.selectbox(
                    "Chosse a method",
                    [
                        "Drop Missing Values",
                        "Fill with mean",
                        "Fill with mode",
                        "Fill with median",
                    ],
                )

            col = []
            if option == "Drop Missing Values":
                col = cleaned_df.columns
            elif option == "Fill with mean" or option == "Fill with median":
                col = cleaned_df.select_dtypes(include="number").columns
            elif option == "Fill with mode":
                col = cleaned_df.select_dtypes(
                    include=["object", "category", "string", "bool"]
                ).columns
            with c2:
                column = st.multiselect("Chosse  column", col)
            if st.button("Apply Cleaning"):
                if option == "Drop Missing Values":
                    cleaned_df = cleaned_df.dropna(subset=column)
                elif option == "Fill with mean":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mean()
                    )
                elif option == "Fill with median":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].median()
                    )
                elif option == "Fill with mode":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mode().iloc[0]
                    )
                st.success("Cleaned Successfully")
                csv = cleaned_df.to_csv(index=False)
                st.download_button(
                    label="Download_Cleaned_Data",
                    data=csv,
                    file_name="Cleaned_data.csv",
                    mime="text/csv",
                )
            st.subheader("Drop Duplicate Rows")
            st.write("Remove duplicate records from your dataset")
            st.metric("Duplicate rows detected", df.duplicated().sum())
            duplicate_opt = st.selectbox(
                "Chosse How To Handle Dupliactes",
                ["Keep first", "Keep last", "Remove all"],
            )
            if duplicate_opt == "Keep first":
                cleaned_df = cleaned_df.drop_duplicates(keep="first")
            elif duplicate_opt == "Keep last":
                cleaned_df = cleaned_df.drop_duplicates(keep="last")
            elif duplicate_opt == "Remove all":
                cleaned_df = cleaned_df.drop_duplicates()
            if st.button("Apply deletion"):
                st.success("Cleaned Successfully")
                csv = cleaned_df.to_csv(index=False)
                st.download_button(
                    label="Download_Cleaned_Data",
                    data=csv,
                    file_name="Cleaned_data.csv",
                    mime="text/csv",
                )

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
            cleaned_df = df.copy()
            with c1:
                option = st.selectbox(
                    "Chosse a method",
                    [
                        "Drop Missing Values",
                        "Fill with mean",
                        "Fill with mode",
                        "Fill with median",
                    ],
                )

            col = []
            if option == "Drop Missing Values":
                col = cleaned_df.columns
            elif option == "Fill with mean" or option == "Fill with median":
                col = cleaned_df.select_dtypes(include="number").columns
            elif option == "Fill with mode":
                col = cleaned_df.select_dtypes(
                    include=["object", "category", "string", "bool"]
                ).columns
            with c2:
                column = st.multiselect("Chosse  column", col)
            if st.button("Apply Cleaning"):
                if option == "Drop Missing Values":
                    cleaned_df = cleaned_df.dropna(subset=column)
                elif option == "Fill with mean":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mean()
                    )
                elif option == "Fill with median":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].median()
                    )
                elif option == "Fill with mode":
                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mode().iloc[0]
                    )
                st.success("Cleaned Successfully")
                csv = cleaned_df.to_excel(index=False)
                st.download_button(
                    label="Download_Cleaned_Data",
                    data=csv,
                    file_name="Cleaned_data.xlsx",
                    mime="text/xlsx",
                )
            st.subheader("Drop Duplicate Rows")
            st.write("Remove duplicate records from your dataset")
            st.metric("Duplicate rows detected", df.duplicated().sum())
            duplicate_opt = st.selectbox(
                "Chosse How To Handle Dupliactes",
                ["Keep first", "Keep last", "Remove all"],
            )
            if duplicate_opt == "Keep first":
                cleaned_df = cleaned_df.drop_duplicates(keep="first")
            elif duplicate_opt == "Keep last":
                cleaned_df = cleaned_df.drop_duplicates(keep="last")
            elif duplicate_opt == "Remove all":
                cleaned_df = cleaned_df.drop_duplicates()
            if st.button("Apply deletion"):
                st.success("Cleaned Successfully")
                csv = cleaned_df.to_excel(index=False)
                st.download_button(
                    label="Download_Cleaned_Data",
                    data=csv,
                    file_name="Cleaned_data.xlsx",
                    mime="text/xlsx",
                )
        else:
            st.error("File type not supported")
elif page == "Visualization":
    st.header("Data Visualization")
    file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
    st.divider()

    st.subheader("Data Visualization")
    st.caption("Create interactive visualization from your dataset")
    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
            chart = st.selectbox(
                "Select Chart Type", ["Bar chart", "Line chart", "Scatter plot"]
            )

            if chart == "Bar chart":
                y_columns = df.select_dtypes(include="number").columns
                x_columns = df.select_dtypes(include=["category", "object"]).columns
                x_axis = st.selectbox("Select Column For X-Axis", x_columns)
                y_axis = st.selectbox("Select Column For Y-Axis", y_columns)
            elif chart == "Line chart":
                y_columns = df.select_dtypes(include="number").columns
                x_columns = df.columns
                x_axis = st.selectbox("Select Column For X-Axis", x_columns)
                y_axis = st.selectbox("Select Column For Y-Axis", y_columns)
            elif chart == "Scatter plot":
                y_columns = df.select_dtypes(include="number").columns
                x_columns = df.select_dtypes(include="number").columns
                x_axis = st.selectbox("Select Column For X-Axis", x_columns)
                y_axis = st.selectbox("Select Column For Y-Axis", y_columns)

            if st.button("Generate Chart"):
                
                fig, ax = plt.subplots(figsize=(10, 5))

                if chart_type == "Bar Chart":

                    chart_data = df.groupby(x_axis)[y_axis].mean()

                    ax.bar(
                        chart_data.index.astype(str),
                        chart_data.values
                    )

                    ax.set_title(f"{y_axis} by {x_axis}")
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)
                    plt.xticks(rotation=45)

                elif chart_type == "Line Chart":

                    ax.plot(
                        df[x_axis],
                        df[y_axis],
                        marker="o"
                    )

                    ax.set_title(f"{y_axis} vs {x_axis}")
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)
                    plt.xticks(rotation=45)

                elif chart_type == "Scatter Plot":

                    ax.scatter(
                        df[x_axis],
                        df[y_axis],
                        alpha=0.7
                    )

                    ax.set_title(f"{y_axis} vs {x_axis}")
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)

                ax.grid(True, alpha=0.3)
                fig.tight_layout()

                st.pyplot(fig)

                plt.close(fig)

            

    else:
        st.info("Please upload a dataset first.")
        
        else:
            st.error("File not supported")



elif page == "Export":
        st.title("📄 Export PDF Report")
        st.write("Generate a PDF report of your dataset.")
        file = st.file_uploader("**Start with your dataset**", type=["csv", "xlsx"])
        st.divider()
        if file:
          if file.name.endswith(".csv"):
           df=pd.read_csv(file)
           cleaned_df=df.copy()
           if df is not None:
    
            buffer = BytesIO()
    
            pdf = canvas.Canvas(buffer, pagesize= A4)
    
            width, height = A4
    
            # Title
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawString(50, height - 60, "Data Lens")
    
            pdf.setFont("Helvetica", 16)
            pdf.drawString(50, height - 90, "Data Analysis Report")
    
            # Date
            pdf.setFont("Helvetica", 10)
            pdf.drawString(
                50, height - 120,
                f"Generated: {datetime.now().strftime('%d-%m-%Y')}"
            )
    
            # Dataset Overview
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(50, height - 170, "Dataset Overview")
    
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, height - 200, f"Total Rows: {len(df)}")
            pdf.drawString(50, height - 225, f"Total Columns: {len(df.columns)}")
            pdf.drawString(50, height - 250, f"Total Cells: {df.size}")
    
            # Data Quality
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(50, height - 300, "Data Quality")
    
            missing = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()
    
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, height - 330, f"Missing Values: {missing}")
            pdf.drawString(50, height - 355, f"Duplicate Rows: {duplicates}")
    
            # Cleaning Summary
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(50, height - 405, "Cleaning Summary")
    
            pdf.setFont("Helvetica", 12)
    
            if cleaned_df is not None:
                pdf.drawString(50, height - 435, f"Rows After Cleaning: {len(cleaned_df)}")
                pdf.drawString(50, height - 460, f"Columns After Cleaning: {len(cleaned_df.columns)}")
                pdf.drawString(
                    50, height - 485,
                    f"Missing Values After Cleaning: {cleaned_df.isnull().sum().sum()}"
                )
            else:
                pdf.drawString(50, height - 435, "No cleaning performed yet.")
    
            # Footer
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(50, 40, "Generated using Data Lens")
    
            pdf.save()
    
            st.download_button(
                "📥 Download PDF Report",
                data=buffer.getvalue(),
                file_name="Data_Lens_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
        else:
            st.warning("Please upload a dataset first.")
        