# NYC Housing & Transportation Dashboard

A Data Engineering and Visualization project exploring borough-level patterns in NYC housing complaints and serious transportation injuries.

## 1. Project Overview

This project combines two datasets from NYC Open Data: one from Housing & Development and one from Transportation.

The goal is to explore how housing complaints and serious transportation injuries vary across New York City's five boroughs over time.

**Research Question:**

How do housing complaints and serious transportation injuries vary across New York City's boroughs over time?

## 2. Datasets

**Dataset 1: Housing — Complaint Problems**

- Dataset ID: `ygpa-z7cr`
- Source: [NYC Open Data — Complaint Problems](https://data.cityofnewyork.us/Housing-Development/Complaint-Problems/ygpa-z7cr)

**Dataset 2: Transportation — SIRTA Data**

- Dataset ID: `xeqp-qz8h`
- Source: [NYC Open Data — SIRTA Data](https://data.cityofnewyork.us/Transportation/Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h)

The SIRTA dataset focuses on serious-injury response records and does not represent all traffic incidents.

## 3. Data Cleaning and Integration

The project includes the following data processing steps:

- Explored both datasets and examined their structure, columns, and missing values.
- Removed exact duplicate records from the transportation dataset.
- Removed transportation records missing essential crash date or borough information.
- Standardized borough names and date formats.
- Extracted years from date columns.
- Aggregated both datasets by borough and year.
- Integrated the datasets using an outer join on borough and year.
- Validated the final integrated dataset for missing values and duplicate records.

The final integrated dataset contains 25 records, representing five NYC boroughs across five years (2022–2026).

**Important:** 2026 data covers January through June only and should not be compared directly with complete years.

Further details about the exploration, cleaning, integration, and analysis are available in the Jupyter Notebook.

## 4. Interactive Dashboard

The project includes an interactive dashboard developed using Python, Streamlit, Pandas, and Plotly.

Dashboard features include:

- Borough selection using dropdown filters.
- Year selection.
- Data domain selection (Housing, Transportation, or Both).
- Search functionality by borough and year.
- A Generate Report button to apply selected filters.
- Summary metrics.
- Interactive housing complaint visualizations.
- Interactive transportation injury visualizations.
- A combined scatter plot exploring the relationship between both datasets.
- A filtered data table.
- Project findings, limitations, and potential benefits for NYC.

## 5. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook
- Git and GitHub

## 6. How to Run the Project Locally

**Step 1:** Clone the repository.

```bash
git clone https://github.com/meralsafwan/NYC-Housing-Transportation.git
cd NYC-Housing-Transportation
```

**Step 2:** Install the required dependencies.

```bash
pip install -r requirements.txt
```

**Step 3:** Run the Streamlit application.

```bash
streamlit run app.py
```

Make sure the integrated CSV file used by `app.py` is located in the same project folder.

## 7. Live Dashboard

The deployed application is available here:

[NYC Housing & Transportation Dashboard](https://nyc-housing-transportation-9iwqtwn7st4ycy9sikvxnh.streamlit.app/)

## 8. Repository Structure

- `app.py` — Main Streamlit dashboard application.
- `NYC_Housing_Transportation_Project.ipynb` — Jupyter Notebook containing data exploration, cleaning, integration, and visualizations.
- `NYC_Integrated_Data.csv` — Integrated borough-year dataset.
- `combined_data.csv` — Additional integrated dataset file.
- `requirements.txt` — Required Python libraries.
- `README.md` — Project documentation.

## 9. Team Contributions

The following table summarizes the responsibilities and contributions of each team member.

| Team Member | Student ID | Contributions |
|---|---|---|
| Member 1: [Name] | [ID] | [Describe actual contributions] |
| Member 2: [Name] | [ID] | [Describe actual contributions] |
| Member 3: [Name] | [ID] | [Describe actual contributions] |
| Member 4: [Name] | [ID] | [Describe actual contributions] |
| Member 5 (if applicable) | [ID] | [Describe actual contributions] |
| Member 6 (if applicable) | [ID] | [Describe actual contributions] |

## 10. Limitations

- The 2026 dataset covers only January through June.
- The analysis is performed at the borough-year level.
- The results identify patterns