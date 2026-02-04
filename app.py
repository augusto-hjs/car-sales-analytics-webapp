import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Car Sales Analytics Webapp", layout="wide")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Create brand from model (first token)
    df["brand"] = (
        df["model"]
        .astype(str)
        .str.strip()
        .str.split()
        .str[0]
        .str.lower()
    )
    return df


car_data = load_data("vehicles.csv")

st.header("Car Sales Analytics Webapp")

# -----------------------------
# Dataset Viewer
# -----------------------------
st.subheader("Dataset Viewer")

dataset_checkbox = st.checkbox("Show Dataset")

if dataset_checkbox:
    st.dataframe(car_data, use_container_width=True)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("Histogram")

if st.checkbox("Create Histogram", value=True):
    fig = px.histogram(
        car_data,
        x="price",
        nbins=40,
        title="Distribution of Vehicle Prices"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Scatter Plot
# -----------------------------
st.subheader("Scatter Plot")

if st.checkbox("Create Scatter", value=True):
    fig = px.scatter(
        car_data,
        x="odometer",
        y="price",
        title="Price vs Odometer"
    )
    st.plotly_chart(fig, use_container_width=True)
