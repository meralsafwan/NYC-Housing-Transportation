
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

        one_year = report_data["year"].nunique() == 1
        one_row = len(report_data) == 1

        # HOUSING VISUALIZATIONS
        if domain in ["Both", "Housing Complaints"]:

            st.subheader("Housing Complaints")

            if one_year:
                fig1 = px.bar(
                    report_data,
                    x="borough",
                    y="unique_complaints",
                    color="borough",
                    title="Housing Complaints by Borough"
                )
            else:
                fig1 = px.line(
                    report_data,
                    x="year",
                    y="unique_complaints",
                    color="borough",
                    markers=True,
                    title="Housing Complaints Over Time"
                )

            st.plotly_chart(fig1, use_container_width=True)

            if one_row:
                st.info(
                    "Only one borough-year is selected. "
                    "The bar chart shows its complaint total."
                )

        # TRANSPORTATION VISUALIZATIONS
        if domain in ["Both", "Transportation Injuries"]:

            st.subheader("Severe Transportation Injuries")

            if one_year:
                fig2 = px.bar(
                    report_data,
                    x="borough",
                    y="total_severe_injuries",
                    color="borough",
                    title="Severe Transportation Injuries by Borough"
                )
            else:
                fig2 = px.line(
                    report_data,
                    x="year",
                    y="total_severe_injuries",
                    color="borough",
                    markers=True,
                    title="Severe Injuries Over Time"
                )

            st.plotly_chart(fig2, use_container_width=True)

            # Heatmap only when there are multiple boroughs and years
            if (
                report_data["borough"].nunique() > 1
                and report_data["year"].nunique() > 1
            ):
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

                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info(
                    "The heatmap is hidden because it needs "
                    "multiple boroughs and multiple years to be useful."
                )

        # COMBINED VISUALIZATION
        if domain == "Both":

            st.subheader("Housing and Transportation Relationship")

            if len(report_data) > 1:
                fig4 = px.scatter(
                    report_data,
                    x="unique_complaints",
                    y="total_severe_injuries",
                    color="borough",
                    symbol="year",
                    hover_data=["borough", "year"],
                    title="Housing Complaints vs Severe Injuries"
                )

                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info(
                    "The relationship chart needs multiple observations. "
                    "Select more boroughs or years to view it."
                )

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

# Use filtered data when a report has been generated
if (
    st.session_state.report_generated
    and not st.session_state.filtered_data.empty
):
    story_data = st.session_state.filtered_data
    story_domain = st.session_state.domain
else:
    story_data = df
    story_domain = "Both"

st.subheader("Key Findings")

if story_domain in ["Both", "Housing Complaints"]:

    housing_averages = (
        story_data.groupby("borough")["unique_complaints"].mean()
    )

    if len(housing_averages) > 1:
        highest = housing_averages.idxmax()
        lowest = housing_averages.idxmin()

        st.write(
            f"- {highest.title()} has the highest average "
            "number of unique housing complaints in the current selection."
        )
        st.write(
            f"- {lowest.title()} has the lowest average "
            "number of unique housing complaints in the current selection."
        )
    elif len(housing_averages) == 1:
        borough = housing_averages.index[0]
        st.write(
            f"- The current housing selection focuses on {borough.title()}."
        )

if story_domain in ["Both", "Transportation Injuries"]:

    transport_averages = (
        story_data.groupby("borough")["total_severe_injuries"].mean()
    )

    if len(transport_averages) > 1:
        highest = transport_averages.idxmax()
        lowest = transport_averages.idxmin()

        st.write(
            f"- {highest.title()} has the highest average "
            "number of severe transportation injuries in the current selection."
        )
        st.write(
            f"- {lowest.title()} has the lowest average "
            "number of severe transportation injuries in the current selection."
        )
    elif len(transport_averages) == 1:
        borough = transport_averages.index[0]
        st.write(
            f"- The current transportation selection focuses on {borough.title()}."
        )

if len(story_data) == 1:
    st.caption(
        "Only one borough-year is selected, so borough comparisons "
        "are not available for this selection."
    )

st.subheader("Limitations")
st.write(
    "The 2026 data covers only January through June. "
    "The analysis identifies patterns and associations, "
    "not causal relationships. The transportation dataset focuses "
    "on serious injury response records, not all traffic incidents."
)

st.subheader("How This Can Benefit NYC")
st.write(
    "The dashboard can help users explore borough-level patterns "
    "and identify areas that may deserve further investigation "
    "by housing and transportation authorities."
)
