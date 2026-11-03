
import streamlit as st
import pandas as pd
import plotly.express as px
import re

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="NYC Housing & Transportation Dashboard",
    page_icon="🏙️",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("NYC_Integrated_Data.csv")

    required_columns = [
        "borough",
        "year",
        "unique_complaints",
        "total_severe_injuries"
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        st.error(f"Missing columns in CSV: {missing}")
        st.stop()

    df["borough"] = df["borough"].astype(str).str.strip().str.upper()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["unique_complaints"] = pd.to_numeric(
        df["unique_complaints"], errors="coerce"
    )
    df["total_severe_injuries"] = pd.to_numeric(
        df["total_severe_injuries"], errors="coerce"
    )

    df = df.dropna(subset=["borough", "year"])
    df["year"] = df["year"].astype(int)

    # Ensure one row per borough and year
    df = (
        df.groupby(["borough", "year"], as_index=False)
        .agg({
            "unique_complaints": "sum",
            "total_severe_injuries": "sum"
        })
    )

    return df


df = load_data()

# -----------------------------
# SESSION STATE
# -----------------------------
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if "filtered_data" not in st.session_state:
    st.session_state.filtered_data = df.copy()

if "domain" not in st.session_state:
    st.session_state.domain = "Both"

# -----------------------------
# TITLE
# -----------------------------
st.title("🏙️ NYC Housing & Transportation Dashboard")

st.write(
    "Explore housing complaints and serious transportation "
    "injuries across New York City's five boroughs."
)

st.info(
    "Note: 2026 data covers January–June only. "
    "It should not be compared directly with complete years."
)

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Report Filters")

with st.sidebar.form("report_filters"):

    borough_choice = st.selectbox(
        "Select Borough",
        ["All Boroughs"] + sorted(df["borough"].unique().tolist())
    )

    year_choice = st.selectbox(
        "Select Year",
        ["All Years"] + sorted(df["year"].unique().tolist())
    )

    domain_choice = st.selectbox(
        "Select Data Domain",
        ["Both", "Housing Complaints", "Transportation Injuries"]
    )

    search_text = st.text_input(
        "Search",
        placeholder="Example: Brooklyn 2022"
    )

    generate = st.form_submit_button("Generate Report")

# -----------------------------
# APPLY FILTERS
# -----------------------------
if generate:

    filtered = df.copy()

    if borough_choice != "All Boroughs":
        filtered = filtered[
            filtered["borough"] == borough_choice.upper()
        ]

    if year_choice != "All Years":
        filtered = filtered[
            filtered["year"] == int(year_choice)
        ]

    # Search by borough and/or year
    if search_text.strip():

        search = search_text.strip().upper()

        matched_boroughs = [
            b for b in df["borough"].unique()
            if b in search
        ]

        matched_years = re.findall(r"\b20\d{2}\b", search)

        # Apply borough search if a borough was entered
        if matched_boroughs:
            filtered = filtered[
                filtered["borough"].isin(matched_boroughs)
            ]

        # Apply year search if a year was entered
        if matched_years:
            filtered = filtered[
                filtered["year"].isin([int(y) for y in matched_years])
            ]

        # Warn if the search contains neither a known borough nor a year
        if not matched_boroughs and not matched_years:
            filtered = filtered.iloc[0:0]

    st.session_state.filtered_data = filtered
    st.session_state.domain = domain_choice
    st.session_state.report_generated = True

# -----------------------------
# DISPLAY REPORT
# -----------------------------
if st.session_state.report_generated:

    report_data = st.session_state.filtered_data
    domain = st.session_state.domain

    st.subheader("Generated Report")

    if report_data.empty:
        st.warning("No data matches your selected filters. Try another search.")

    else:

        # SUMMARY METRICS
        col1, col2 = st.columns(2)

        if domain in ["Both", "Housing Complaints"]:
            col1.metric(
                "Unique Housing Complaints",
                f"{report_data['unique_complaints'].sum():,.0f}"
            )

        if domain in ["Both", "Transportation Injuries"]:
            col2.metric(
                "Severe Transportation Injuries",
                f"{report_data['total_severe_injuries'].sum():,.0f}"
            )

        st.divider()

        # -----------------------------
        # HOUSING CHARTS
        # -----------------------------
        if domain in ["Both", "Housing Complaints"]:

            st.header("Housing Complaints")

            # Line chart - works with one or many points
            fig1 = px.line(
                report_data,
                x="year",
                y="unique_complaints",
                color="borough",
                markers=True,
                title="Housing Complaints Over Time"
            )

            st.plotly_chart(fig1, use_container_width=True)

            # Bar chart - works even with one borough and one year
            fig2 = px.bar(
                report_data,
                x="borough",
                y="unique_complaints",
                color="borough",
                hover_data=["year"],
                title="Housing Complaints by Borough"
            )

            st.plotly_chart(fig2, use_container_width=True)

        # -----------------------------
        # TRANSPORTATION CHARTS
        # -----------------------------
        if domain in ["Both", "Transportation Injuries"]:

            st.header("Severe Transportation Injuries")

            # Line chart
            fig3 = px.line(
                report_data,
                x="year",
                y="total_severe_injuries",
                color="borough",
                markers=True,
                title="Severe Transportation Injuries Over Time"
            )

            st.plotly_chart(fig3, use_container_width=True)

            # Bar chart
            fig4 = px.bar(
                report_data,
                x="borough",
                y="total_severe_injuries",
                color="borough",
                hover_data=["year"],
                title="Severe Injuries by Borough"
            )

            st.plotly_chart(fig4, use_container_width=True)

            # Heatmap
            heatmap_data = report_data.pivot(
                index="borough",
                columns="year",
                values="total_severe_injuries"
            )

            fig5 = px.imshow(
                heatmap_data,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="YlOrRd",
                title="Severe Transportation Injuries Heatmap"
            )

            st.plotly_chart(fig5, use_container_width=True)

        # -----------------------------
        # COMBINED VISUALIZATION
        # -----------------------------
        if domain == "Both":

            st.header("Housing and Transportation Relationship")

            fig6 = px.scatter(
                report_data,
                x="unique_complaints",
                y="total_severe_injuries",
                color="borough",
                symbol="year",
                hover_data=["borough", "year"],
                title="Housing Complaints vs Severe Injuries"
            )

            st.plotly_chart(fig6, use_container_width=True)

            st.caption(
                "Each point represents one borough in one year. "
                "A single selected result appears as one point."
            )

        # -----------------------------
        # FILTERED DATA TABLE
        # -----------------------------
        st.subheader("Filtered Data")

        st.dataframe(
            report_data,
            use_container_width=True,
            hide_index=True
        )

        # Download filtered results
        csv = report_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Filtered Data",
            data=csv,
            file_name="NYC_filtered_data.csv",
            mime="text/csv"
        )

else:
    st.info(
        "Choose your filters in the sidebar and click "
        "'Generate Report' to view the dashboard."
    )

# -----------------------------
# PROJECT STORY
# -----------------------------
st.divider()
st.header("Project Story")

st.subheader("Research Question")

st.write(
    "How do housing complaints and serious transportation "
    "injuries vary across New York City's boroughs over time?"
)

# Use all data for overall findings
st.subheader("Key Findings")

housing_averages = (
    df.groupby("borough")["unique_complaints"].mean()
)

transport_averages = (
    df.groupby("borough")["total_severe_injuries"].mean()
)

if not housing_averages.empty:
    st.write(
        f"- {housing_averages.idxmax().title()} has the highest "
        "average number of unique housing complaints per borough-year."
    )

if not transport_averages.empty:
    st.write(
        f"- {transport_averages.idxmax().title()} has the highest "
        "average number of severe transportation injuries per borough-year."
    )

if not housing_averages.empty and not transport_averages.empty:
    st.write(
        f"- {housing_averages.idxmin().title()} has the lowest "
        "average housing complaints, while "
        f"{transport_averages.idxmin().title()} has the lowest "
        "average severe transportation injuries."
    )

st.subheader("Limitations")

st.write(
    "The 2026 data covers only January through June. "
    "The analysis identifies patterns and associations, "
    "not causal relationships. The transportation dataset "
    "focuses on serious injury response records, not all traffic incidents."
)

st.subheader("How This Can Benefit NYC")

st.write(
    "The dashboard can help users explore borough-level patterns "
    "and identify areas that may deserve further investigation "
    "by housing and transportation authorities."
)
