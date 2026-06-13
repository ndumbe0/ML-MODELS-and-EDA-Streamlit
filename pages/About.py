import streamlit as st


def show():
    st.title("About")
    st.markdown("""
    ## Telco Churn Analysis & Prediction Platform

    **Built with:**
    - Streamlit
    - scikit-learn
    - Plotly
    - Pandas

    **ML Models Implemented:**
    1. Random Forest
    2. Logistic Regression
    3. Gradient Boosting
    4. Support Vector Machine (SVM)
    5. K-Nearest Neighbors (KNN)

    Each model includes:
    - Automated preprocessing pipelines
    - Cross-validation
    - Hyperparameter tuning via GridSearchCV/RandomizedSearchCV
    - Performance metrics and visualizations

    **Developer:** Moses N Ndumbe  
    **Team Lead:** Ms. Portia Bentum  
    **Organization:** Azubi Africa
    """)
