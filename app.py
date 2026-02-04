import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Car Sales Analytics Webapp", layout="wide")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load dataset and create derived columns used by the app."""
    df = pd.read_csv(path)

    # Create 'brand' from the first token of the 'model' column
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
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

# Default brand = most common brand in the dataset
default_brand = car_data["brand"].value_counts().idxmax()

brands = sorted(car_data["brand"].dropna().unique())
brand_selected = st.sidebar.selectbox(
    "Brand",
    brands,
    index=brands.index(default_brand) if default_brand in brands else 0,
)

type_options = ["All"]
if "type" in car_data.columns:
    type_options += sorted(car_data["type"].dropna().unique())

type_selected = st.sidebar.selectbox("Vehicle Type", type_options, index=0)

# Apply filters (keep the raw filtered set first)
df_filtered = car_data[car_data["brand"] == brand_selected].copy()

if type_selected != "All" and "type" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["type"] == type_selected]

# Prepare datasets for each visualization
# - Histogram + price KPIs only need 'price'
df_base = df_filtered.dropna(subset=["price"]).copy()

# - Scatter + odometer KPI needs both 'price' and 'odometer'
df_scatter = df_base.dropna(subset=["odometer"]).copy()

# -----------------------------
# KPI row
# -----------------------------
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Listings", f"{len(df_filtered):,}")
kpi2.metric(
    "Median price",
    f"${df_base['price'].median():,.0f}" if len(df_base) else "—"
)
kpi3.metric(
    "Median odometer",
    f"{df_scatter['odometer'].median():,.0f}" if len(df_scatter) else "—"
)

# -----------------------------
# Dataset Viewer
# -----------------------------
st.subheader("Dataset Viewer")
if st.checkbox("Show Dataset"):
    # Show the filtered dataset (even if some columns have missing values)
    st.dataframe(df_filtered.head(50), use_container_width=True)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("Histogram")
if st.checkbox("Create Histogram", value=True):
    if len(df_base) == 0:
        st.info(
            "No rows with price available for this selection, so the histogram can't be displayed.")
    else:
        fig = px.histogram(
            df_base,
            x="price",
            nbins=40,
            title=f"Distribution of Vehicle Prices — {str(brand_selected).title()}",
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Scatter
# -----------------------------
st.subheader("Scatter Plot")
if st.checkbox("Create Scatter", value=True):
    if len(df_scatter) == 0:
        st.info(
            "No rows with odometer available for this selection, so the scatter plot can't be displayed.")
    else:
        fig = px.scatter(
            df_scatter,
            x="odometer",
            y="price",
            title=f"Price vs Odometer — {str(brand_selected).title()}",
            hover_data=["model_year", "condition",
                        "type", "fuel", "transmission"],
        )
        st.plotly_chart(fig, use_container_width=True)
