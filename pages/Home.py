import streamlit as st


def show():
    st.title("Telco Churn Analysis & Prediction")
    st.markdown("""
    ## Welcome to the ML-Powered Telco Churn Platform

    This application combines **Exploratory Data Analysis (EDA)** and **Machine Learning** to help telecommunications companies understand and predict customer churn.

    ### What you can do:
    - 📊 **Explore Data**: Interactive EDA with histograms, boxplots, correlation heatmaps, and pairplots
    - 🤖 **Train Models**: Compare 5 ML algorithms with cross-validation and hyperparameter tuning
    - 🔮 **Make Predictions**: Predict customer churn with probability scores
    - 📥 **Download Results**: Export cleaned data, model predictions, and visualizations
    - 🤖 **AI Assistant**: Ask Gemini AI to explain model results or EDA findings

    ### Dataset
    The app uses the **Telco Customer Churn** dataset, which contains customer information including:
    - Demographics (gender, senior citizen status)
    - Account information (contract type, payment method)
    - Services subscribed (internet, phone, streaming)
    - Billing information (monthly and total charges)

    ### Getting Started
    Use the sidebar to navigate between pages. Upload your dataset or use the default Telco data.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Features", "19", "After preprocessing")
    with col2:
        st.metric("ML Models", "5", "With CV & tuning")
    with col3:
        st.metric("Target", "Churn (Yes/No)", "Binary classification")
