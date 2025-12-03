"""
Streamlit Interactive Dashboard
Showcases: User Selections for Charts
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Interactive Dashboard", layout="wide")

st.title("📊 Interactive Data Dashboard")
st.caption("Showcasing: Streamlit User Selections for Charts")

# Generate sample data
np.random.seed(42)
df = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D', 'E'],
    'Sales': np.random.randint(100, 1000, 5),
    'Profit': np.random.randint(10, 200, 5),
    'Region': ['North', 'South', 'East', 'West', 'Central']
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product")
    # Bar chart with selection
    event = st.bar_chart(df.set_index('Product')['Sales'], use_container_width=True)

with col2:
    st.subheader("Profit Analysis")
    st.line_chart(df.set_index('Product')['Profit'], use_container_width=True)

# Data table with frozen columns
st.subheader("📋 Data Table")
st.dataframe(
    df,
    column_config={
        "Sales": st.column_config.NumberColumn("Sales ($)", format="$%d"),
        "Profit": st.column_config.ProgressColumn("Profit", max_value=200)
    },
    use_container_width=True
)

# Interactive filters
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect("Select Regions", df['Region'].unique(), default=df['Region'].unique())
filtered_df = df[df['Region'].isin(selected_regions)]

st.subheader("Filtered Results")
st.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
st.metric("Avg Profit", f"${filtered_df['Profit'].mean():.0f}")
