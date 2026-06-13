import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.visualizations import (
    plot_histogram, plot_boxplot, plot_correlation_heatmap,
    plot_pairplot, plot_churn_distribution, plot_missing_values
)


def show():
    st.title("Exploratory Data Analysis")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx', 'xls'], key="eda_upload")
    df = load_data(uploaded_file=uploaded_file)
    if df is None:
        return

    st.sidebar.subheader("Filters")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    with st.expander("Dataset Overview"):
        st.dataframe(df.head(100))
        st.write(f"**Shape:** {df.shape}")
        st.write(f"**Columns:** {list(df.columns)}")
        st.write(f"**Missing values:** {df.isnull().sum().sum()}")
        st.write(df.describe(include='all'))

    st.markdown("---")
    plot_missing_values(df)

    col1, col2 = st.columns(2)
    with col1:
        plot_churn_distribution(df)
    with col2:
        if numeric_cols:
            plot_histogram(df, numeric_cols[0], f"Distribution of {numeric_cols[0]}")

    if cat_cols:
        st.subheader("Categorical Analysis")
        cat = st.selectbox("Select categorical column", cat_cols)
        fig = px.bar(df[cat].value_counts().reset_index(), x=cat, y='count', title=f"{cat} Distribution")
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation Heatmap")
    if numeric_cols:
        plot_correlation_heatmap(df, numeric_cols)

    st.subheader("Boxplots by Churn")
    num_for_box = st.selectbox("Select numeric column", numeric_cols)
    plot_boxplot(df, 'Churn', num_for_box, f"{num_for_box} by Churn")

    if st.checkbox("Show Pairplot (may be slow)"):
        selected = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:3])
        if len(selected) >= 2:
            plot_pairplot(df, selected, 'Churn')

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")
