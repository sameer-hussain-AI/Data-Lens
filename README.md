# Data Lens

**An interactive data analysis and cleaning application built with
Python and Streamlit.**

Data Lens helps users upload tabular datasets, inspect their structure
and quality, clean common data issues, create visualizations, and export
the processed results through a simple web interface.

## Features

### 1. Dataset upload

-   Upload CSV and Excel (`.xlsx`) files.
-   Load a dataset into the application for analysis.

### 2. Dataset overview

-   View key dataset information, including row and column counts.
-   Get a quick understanding of the uploaded dataset.

### 3. Data preview

-   Preview dataset records.
-   Select columns to inspect.
-   Search for records in the dataset.

### 4. Data quality

-   Inspect missing values.
-   Review duplicate records.
-   Examine column data types and unique values.
-   View dataset completeness information.

### 5. Data cleaning

-   Handle missing values using suitable strategies for numerical and
    categorical columns.
-   Remove selected columns when they are not needed.
-   Apply cleaning operations to the working dataset and review the
    result.

### 6. Data visualization

Create charts from selected dataset columns: - Bar chart - Line chart -
Scatter plot - Histogram

### 7. Export

-   Download the cleaned dataset.
-   Generate a PDF report of the analysis, where enabled in the
    application.

## Technology stack

-   **Python** --- application logic
-   **Streamlit** --- interactive web interface
-   **Pandas** --- data loading, manipulation, and analysis
-   **Openpyxl** --- Excel workbook support
-   **ReportLab** --- PDF report generation

## Project structure

``` text
Data-Lens/
├── app.py
├── requirements.txt
├── README.md
└── logo.png
```

The exact files in your repository may vary. Keep `app.py` and
`requirements.txt` in the repository root for the deployment
instructions below.

## Run locally

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/Data-Lens.git
cd Data-Lens
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment (recommended)

**Windows:**

``` bash
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

``` bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal, usually
`http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1.  Push this repository to GitHub.
2.  Open [Streamlit Community Cloud](https://share.streamlit.io/).
3.  Sign in with GitHub and select **Create app**.
4.  Choose this repository and the `main` branch.
5.  Set the main file path to `app.py`.
6.  Select **Deploy**.

Keep `requirements.txt` in the repository root so the deployment service
can install the application's dependencies.

## Usage

1.  Open Data Lens.
2.  Upload a CSV or Excel dataset.
3.  Explore the overview, preview, and data-quality information.
4.  Choose the cleaning operations you need and apply them.
5.  Select a chart type and the relevant columns to visualize the data.
6.  Export the cleaned dataset or report using the available export
    options.

## Notes

-   The available operations depend on the uploaded file and its column
    types.
-   Review cleaning choices before applying them, as removing rows or
    columns and filling missing values can change the dataset.
-   Do not upload confidential or sensitive datasets to a public
    deployment unless you have assessed the privacy and security
    implications.
-   For reliable deployment, keep the dependency list in
    `requirements.txt` aligned with the packages imported by `app.py`.

## Author

**Sameer Hussain**

Aspiring Data Analyst \| Python \| Pandas \| Power BI \| Excel \| SQL \|
AI

-   GitHub: [sameer-hussain-AI](https://github.com/sameer-hussain-AI)
-   LinkedIn: [Sameer
    Hussain](https://www.linkedin.com/in/sameer-hussain-920722356/)

------------------------------------------------------------------------

*Data Lens --- making dataset exploration and cleaning more accessible.*
