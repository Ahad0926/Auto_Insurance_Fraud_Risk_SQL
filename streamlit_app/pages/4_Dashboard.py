import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

# Title and description
st.title("Dashboard")
st.markdown("""
This tool allows you to explore specific customer segments based on demographic and behavioural filters.
You can filter by risk score, age, income, credit score, and driving experience to examine claim behaviour, risk patterns, and segment composition.
""")

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("Segment Filters")
risk_range = st.sidebar.slider("Risk Score Range", 0, 5, (0, 5))
age_options = st.sidebar.multiselect("Age Group", ["16-25", "26-39", "40-64", "65+"], default=["16-25", "26-39", "40-64", "65+"])
income_options = st.sidebar.multiselect("Income Bracket", ["poverty", "working class", "middle class", "upper class"],
                                        default=["poverty", "working class", "middle class", "upper class"])
experience_options = st.sidebar.multiselect("Driving Experience", ["0-9y", "10-19y", "20-29y", "30y+"],
                                            default=["0-9y", "10-19y", "20-29y", "30y+"])
credit_range = st.sidebar.slider("Credit Score Range", 0.0, 1.0, (0.0, 1.0))

# ---------------------------
# SQL generator
# ---------------------------
def build_sql_from_filters():
    query = """
    SELECT rs.id, rs.risk_score, c.age, c.income, c.credit_score, d.driving_experience, cl.outcome
    FROM risk_scores rs
    JOIN customers c ON rs.id = c.id
    JOIN driving_history d ON rs.id = d.id
    JOIN claims cl ON rs.id = cl.id
    WHERE 1=1
    """
    if age_options:
        age_str = ",".join(f"'{a}'" for a in age_options)
        query += f"\nAND c.age IN ({age_str})"
    if income_options:
        inc_str = ",".join(f"'{i}'" for i in income_options)
        query += f"\nAND c.income IN ({inc_str})"
    if experience_options:
        exp_str = ",".join(f"'{e}'" for e in experience_options)
        query += f"\nAND d.driving_experience IN ({exp_str})"
    if risk_range != (0, 5):
        query += f"\nAND rs.risk_score BETWEEN {risk_range[0]} AND {risk_range[1]}"
    if credit_range != (0.0, 1.0):
        query += f"\nAND c.credit_score BETWEEN {credit_range[0]} AND {credit_range[1]}"
    query += "\nORDER BY rs.risk_score DESC, cl.outcome DESC;"
    return query

# ---------------------------
# Load filtered data
# ---------------------------
@st.cache_data
def load_segment(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

sql_query = build_sql_from_filters()
segment = load_segment(sql_query)

# ---------------------------
# Summary metrics
# ---------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{len(segment):,}")
col2.metric("Avg. Risk Score", f"{segment['risk_score'].mean():.2f}")
col3.metric("Claim Rate", f"{segment['outcome'].mean() * 100:.2f}%")
col4.metric("Avg. Credit Score", f"{segment['credit_score'].mean():.2f}")

# ---------------------------
# Two-column layout: Table | Visuals
# ---------------------------
main_col1, main_col2 = st.columns([1, 1])

# --- Left: Data table ---
with main_col1:
    st.subheader("Filtered Segment Table")
    st.dataframe(segment, use_container_width=True)

    csv = segment.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Segment as CSV", csv, "segment.csv", "text/csv")

    with st.expander("View underlying SQL template"):
        st.code(sql_query.strip(), language="sql")

# --- Right: Visualizations ---
with main_col2:
    st.subheader("Segment Composition")
    vis_col1, vis_col2 = st.columns([1, 1])

    with vis_col1:
        # Bar chart: Age distribution
        age_counts = segment["age"].value_counts().reset_index()
        age_counts.columns = ["age", "count"]
        age_order = ["16-25", "26-39", "40-64", "65+"]
        age_counts["age"] = pd.Categorical(age_counts["age"], categories=age_order, ordered=True)
        age_counts = age_counts.sort_values("age")

        age_fig = px.bar(
            age_counts, x="age", y="count",
            labels={"age": "Age Group", "count": "Count"},
            title="Age Distribution",
            color_discrete_sequence=px.colors.sequential.Teal_r
        )
        age_fig.update_layout(height=300)
        age_fig.update_layout(title={'x': 0.4})
        st.plotly_chart(age_fig, use_container_width=True)

        # Horizontal Bar Chart: Customers per Risk Score
        risk_counts = segment["risk_score"].value_counts().reset_index()
        risk_counts.columns = ["risk_score", "count"]
        risk_counts = risk_counts.sort_values("risk_score")

        risk_fig = px.bar(
            risk_counts, x="count", y="risk_score", orientation="h",
            labels={"risk_score": "Risk Score", "count": "Customers"},
            title="Customers per Risk Score",
            color_discrete_sequence=px.colors.sequential.Teal_r
        )
        risk_fig.update_layout(height=300)
        risk_fig.update_layout(title={'x': 0.3})
        st.plotly_chart(risk_fig, use_container_width=True)

    with vis_col2:
        # Pie chart 1: Income
        income_counts = segment["income"].value_counts().reset_index()
        income_counts.columns = ["income", "count"]

        income_fig = px.pie(
            income_counts, names="income", values="count",
            title="Income Bracket Distribution",
            color_discrete_sequence=px.colors.sequential.PuBu_r
        )
        income_fig.update_layout(height=300)
        income_fig.update_layout(title={'x': 0.25})
        st.plotly_chart(income_fig, use_container_width=True)

        # Pie chart 2: Claims
        outcome_counts = segment["outcome"].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]
        outcome_counts["Outcome"] = outcome_counts["Outcome"].map({0: "No Claim", 1: "Filed Claim"})

        outcome_fig = px.pie(
            outcome_counts, names="Outcome", values="Count",
            title="Claim Outcome Distribution",
            color_discrete_sequence=px.colors.sequential.PuBu_r
        )
        outcome_fig.update_layout(height=300)
        outcome_fig.update_layout(title={'x': 0.25})
        st.plotly_chart(outcome_fig, use_container_width=True)