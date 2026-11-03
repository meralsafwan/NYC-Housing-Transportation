
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
    df["borough"] = df["borough"].str.strip().str.upper()
    df["year"] = df["year"].astype(int)
    df["unique_complaints"] = pd.to_numeric(
        df["unique_complaints"], errors="coerce"
    )
    df["total_severe_injuries"] = pd.to_numeric(
        df["total_severe_injuries"], errors="coerce"
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
if generate:

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
            borough for borough in df["borough"].unique()
            if borough in search
        ]

        matched_years = re.findall(r"\b20\d{2}\b", search)

        if matched_boroughs:
            filtered = filtered[
                filtered["borough"].isin(matched_boroughs)
            ]

        if matched_years:
            filtered = filtered[
                filtered["year"].isin(
                    [int(year) for year in matched_years]
                )
            ]

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

        st.warning("No data matches your selected filters.")

    else:

        # SUMMARY METRICS
        col1, col2 = st.columns(2)

        if domain in ["Both", "Housing Complaints"]:
            with col1:
                st.metric(
                    "Unique Housing Complaints",
                    f"{report_data['unique_complaints'].sum():,.0f}"
                )

        if domain in ["Both", "Transportation Injuries"]:
            with col2:
                st.metric(
                    "Severe Transportation Injuries",
                    f"{report_data['total_severe_injuries'].sum():,.0f}"
                )

        st.divider()

        borough_count = report_data["borough"].nunique()
        year_count = report_data["year"].nunique()
        row_count = len(report_data)

        # -----------------------------
        # HOUSING CHARTS
        # -----------------------------
        if domain in ["Both", "Housing Complaints"]:

            st.subheader("Housing Complaints")

            if borough_count > 1 and year_count > 1:

                fig1 = px.line(
                    report_data,
                    x="year",
                    y="unique_complaints",
                    color="borough",
                    markers=True,
                    title="Housing Complaints Over Time"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

                fig2 = px.bar(
                    report_data,
                    x="borough",
                    y="unique_complaints",
                    color="borough",
                    title="Housing Complaints by Borough and Year",
                    barmode="group"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            elif borough_count > 1:

                fig1 = px.bar(
                    report_data,
                    x="borough",
                    y="unique_complaints",
                    color="borough",
                    title="Housing Complaints by Borough"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

            elif year_count > 1:

                fig1 = px.line(
                    report_data,
                    x="year",
                    y="unique_complaints",
                    markers=True,
                    title="Housing Complaints Over Time"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

            else:
                st.info(
                    "One borough and one year selected. "
                    "The housing total is shown above."
                )

        # -----------------------------
        # TRANSPORTATION CHARTS
        # -----------------------------
        if domain in ["Both", "Transportation Injuries"]:

            st.subheader("Severe Transportation Injuries")

            if borough_count > 1 and year_count > 1:

                fig2 = px.line(
                    report_data,
                    x="year",
                    y="total_severe_injuries",
                    color="borough",
                    markers=True,
                    title="Severe Injuries Over Time"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            elif borough_count > 1:

                fig2 = px.bar(
                    report_data,
                    x="borough",
                    y="total_severe_injuries",
                    color="borough",
                    title="Severe Injuries by Borough"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            elif year_count > 1:

                fig2 = px.line(
                    report_data,
                    x="year",
                    y="total_severe_injuries",
                    markers=True,
                    title="Severe Injuries Over Time"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            else:
                st.info(
                    "One borough and one year selected. "
                    "The transportation total is shown above."
                )

            # Heatmap needs multiple boroughs and years
            if borough_count > 1 and year_count > 1:

                heatmap_data = report_data.pivot(
                    index="borough",
                    columns="year",
                    values="total_severe_injuries"
                )

                fig3 = px.imshow(
                    heatmap_data,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="YlOrRd",
                    title="Severe Transportation Injuries Heatmap"
                )

                st.plotly_chart(
                    fig3,
                    use_container_width=True
                )

        # -----------------------------
        # COMBINED VISUALIZATION
        # -----------------------------
        if domain == "Both":

            st.subheader("Housing and Transportation Relationship")

            if row_count > 1:

                fig4 = px.scatter(
                    report_data,
                    x="unique_complaints",
                    y="total_severe_injuries",
                    color="borough",
                    symbol="year",
                    hover_data=["borough", "year"],
                    title="Housing Complaints vs Severe Injuries"
                )

                st.plotly_chart(
                    fig4,
                    use_container_width=True
                )

            else:
                st.info(
                    "Select more boroughs or years to explore "
                    "the relationship between both datasets."
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

# Use current report selection when available
if st.session_state.report_generated:

    story_data = st.session_state.filtered_data
    story_domain = st.session_state.domain

else:

    story_data = df.copy()
    story_domain = "Both"

st.subheader("Key Findings")

if story_data.empty:

    st.write(
        "No findings are available because no data matches "
        "the current selection."
    )

else:

    # Housing findings
    if story_domain in ["Both", "Housing Complaints"]:

        housing_averages = (
            story_data.groupby("borough")["unique_complaints"].mean()
        )

        if len(housing_averages) > 1:

            highest = housing_averages.idxmax()
            lowest = housing_averages.idxmin()

            st.write(
                f"- {highest.title()} has the highest average "
                "number of unique housing complaints in this selection."
            )

            st.write(
                f"- {lowest.title()} has the lowest average "
                "number of unique housing complaints in this selection."
            )

        elif len(housing_averages) == 1:

            borough = housing_averages.index[0]

            st.write(
                f"- The selected housing data focuses on {borough.title()}. "
                "There is only one borough, so a borough comparison "
                "is not available."
            )

    # Transportation findings
    if story_domain in ["Both", "Transportation Injuries"]:

        transport_averages = (
            story_data.groupby("borough")[
                "total_severe_injuries"
            ].mean()
        )

        if len(transport_averages) > 1:

            highest = transport_averages.idxmax()
            lowest = transport_averages.idxmin()

            st.write(
                f"- {highest.title()} has the highest average "
                "number of severe transportation injuries "
                "in this selection."
            )

            st.write(
                f"- {lowest.title()} has the lowest average "
                "number of severe transportation injuries "
                "in this selection."
            )

        elif len(transport_averages) == 1:

            borough = transport_averages.index[0]

            st.write(
                f"- The selected transportation data focuses on "
                f"{borough.title()}. A borough comparison is not available."
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
