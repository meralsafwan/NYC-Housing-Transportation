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
    df["borough"] = df["borough"].str.upper()
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("🏙️ NYC Housing & Transportation Dashboard")

st.write(
    "Explore housing complaints and severe transportation "
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
        [
            "Both",
            "Housing Complaints",
            "Transportation Injuries"
        ]
    )

    search_text = st.text_input(
        "Search",
        placeholder="Example: Brooklyn 2022"
    )

    generate = st.form_submit_button("Generate Report")

# -----------------------------
# APPLY FILTERS
# -----------------------------
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if generate:
    st.session_state.report_generated = True
    filtered = df.copy()

    if borough_choice != "All Boroughs":
        filtered = filtered[
            filtered["borough"] == borough_choice
        ]

    if year_choice != "All Years":
        filtered = filtered[
            filtered["year"] == int(year_choice)
        ]

    # Search by borough and/or year
    if search_text.strip():
        search = search_text.upper()

        matched_boroughs = [
            b for b in df["borough"].unique()
            if b in search
        ]

        matched_years = re.findall(
            r"\b20\d{2}\b", search
        )

        if matched_boroughs:
            filtered = filtered[
                filtered["borough"].isin(matched_boroughs)
            ]

        if matched_years:
            filtered = filtered[
                filtered["year"].isin(
                    [int(y) for y in matched_years]
                )
            ]

    st.session_state.filtered_data = filtered
    st.session_state.domain = domain_choice

# -----------------------------
# DISPLAY REPORT
# -----------------------------
if st.session_state.report_generated:

    report_data = st.session_state.filtered_data
    domain = st.session_state.domain

    st.subheader("Generated Report")

    if report_data.empty:
        st.warning("No data matches your selected filters.")

    else:
        # Summary numbers
        col1, col2 = st.columns(2)

        if domain in ["Both", "Housing Complaints"]:
            with col1:
                st.metric(
                    "Unique Housing Complaints",
                    f"{report_data['unique_complaints'].sum():,}"
                )

        if domain in ["Both", "Transportation Injuries"]:
            with col2:
                st.metric(
                    "Severe Transportation Injuries",
                    f"{report_data['total_severe_injuries'].sum():,}"
                )

        st.divider()

        # Housing line chart
        if domain in ["Both", "Housing Complaints"]:
            st.subheader("Housing Complaints by Borough")

            fig1 = px.line(
                report_data,
                x="year",
                y="unique_complaints",
                color="borough",
                markers=True,
                title="Housing Complaints Over Time"
            )

            st.plotly_chart(fig1, use_container_width=True)

            # Housing bar chart
            fig2 = px.bar(
                report_data,
                x="borough",
                y="unique_complaints",
                color="borough",
                title="Housing Complaints by Borough"
            )

            st.plotly_chart(fig2, use_container_width=True)

        # Transportation line chart and heatmap
        if domain in ["Both", "Transportation Injuries"]:
            st.subheader("Severe Transportation Injuries")

            fig3 = px.line(
                report_data,
                x="year",
                y="total_severe_injuries",
                color="borough",
                markers=True,
                title="Severe Injuries Over Time"
            )

            st.plotly_chart(fig3, use_container_width=True)

            heatmap_data = report_data.pivot(
                index="borough",
                columns="year",
                values="total_severe_injuries"
            )

            fig4 = px.imshow(
                heatmap_data,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="YlOrRd",
                title="Severe Injuries Heatmap"
            )

            st.plotly_chart(fig4, use_container_width=True)

        # Combined visualization
        if domain == "Both":
            st.subheader("Housing and Transportation Relationship")

            fig5 = px.scatter(
                report_data,
                x="unique_complaints",
                y="total_severe_injuries",
                color="borough",
                symbol="year",
                hover_data=["borough", "year"],
                title="Housing Complaints vs Severe Injuries"
            )

            st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Filtered Data")
        st.dataframe(report_data, use_container_width=True)

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
    "How do housing complaints and severe transportation "
    "injuries vary across New York City's boroughs over time?"
)

st.subheader("Key Findings")
st.write(
    "- The Bronx recorded the highest average housing complaints "
    "in our aggregated data."
)
st.write(
    "- Brooklyn recorded the highest average severe transportation injuries."
)
st.write(
    "- Staten Island recorded the lowest averages in both measurements."
)

st.subheader("Limitations")
st.write(
    "The 2026 data covers only January through June. "
    "The analysis identifies patterns and associations, "
    "not causal relationships."
)

st.subheader("How This Can Benefit NYC")
st.write(
    "The dashboard can help users explore borough-level patterns "
    "and identify areas that may deserve further investigation "
    "by housing and transportation authorities."
)
