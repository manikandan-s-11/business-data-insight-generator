import streamlit as st
import pandas as pd

st.title("Business Data Insight Generator")

# Upload file
file = st.file_uploader("Upload CSV File", type=["csv"])

# Stop if no file
if file is None:
    st.info("👆 Please upload a CSV file to start analysis")
    st.stop()

# Read data
data = pd.read_csv(file)

# ---------------- DATA PREVIEW ----------------
st.subheader("Data Preview")
st.dataframe(data)

# ---------------- FILTER ----------------
st.subheader("Filter Data")

filter_column = st.selectbox("Select column to filter", data.columns)

search_value = st.text_input("Type to search")

if search_value:
    filtered_data = data[data[filter_column].astype(str).str.contains(search_value, case=False)]
else:
    filtered_data = data

st.write("Filtered Data")
st.dataframe(filtered_data)

# ---------------- DOWNLOAD BUTTON ----------------
csv = filtered_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ---------------- KEY METRICS ----------------
st.subheader("Key Metrics")

if "Sales" in filtered_data.columns:
    total = filtered_data["Sales"].sum()
    average = filtered_data["Sales"].mean()
    count = filtered_data.shape[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", total)
    col2.metric("Average Sales", round(average, 2))
    col3.metric("Count", count)

# ---------------- GROUP ANALYSIS ----------------
st.subheader("Group Analysis")

group_column = st.selectbox("Select column to group by", data.columns)

if group_column != "Sales" and "Sales" in data.columns:
    group_data = filtered_data.groupby(group_column)["Sales"].sum()

    st.bar_chart(group_data)

    # ---------------- TOP INSIGHTS ----------------
    st.subheader("Top Insights")

    top_value = group_data.idxmax()
    top_sales = group_data.max()

    st.success(f"Top {group_column}: {top_value} (Sales: {top_sales})")

    # EXTRA: Overall Top Product & Region (Fixed version)
    
    if "Region" in filtered_data.columns:
        region_sales = filtered_data.groupby("Region")["Sales"].sum()
        st.info(f"Top Region: {region_sales.idxmax()} ({region_sales.max()})")

else:
    st.warning("Please select a valid column (not 'Sales')")