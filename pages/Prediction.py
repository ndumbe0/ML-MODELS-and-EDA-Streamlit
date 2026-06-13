import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


def show():
    st.title("Churn Prediction")
    uploaded_file = st.sidebar.file_uploader("Upload dataset", type=['csv', 'xlsx'], key="pred_upload")
    df = load_data(uploaded_file=uploaded_file)
    if df is None:
        return

    if 'model_results' not in st.session_state:
        st.warning("Please train models first on the Model Training page.")
        return

    results = st.session_state['model_results']
    model_names = list(results.keys())
    selected = st.selectbox("Select Model", model_names)
    model = results[selected]['model']

    st.subheader("Enter Customer Details")
    X = df.drop('Churn', axis=1)
    cols = st.columns(3)
    input_data = {}
    for i, col in enumerate(X.columns):
        with cols[i % 3]:
            if X[col].dtype == 'object':
                input_data[col] = st.selectbox(col, options=X[col].unique())
            else:
                min_val = float(X[col].min())
                max_val = float(X[col].max())
                input_data[col] = st.number_input(col, min_value=min_val, max_value=max_val, value=float(X[col].median()))

    if st.button("Predict", type="primary"):
        input_df = pd.DataFrame([input_data])
        try:
            _, _, preprocessor, le = preprocess_data(df)
            processed = preprocessor.transform(input_df)
            pred = model.predict(processed)[0]
            proba = model.predict_proba(processed)[0][1] if hasattr(model, 'predict_proba') else None
            churn_label = le.inverse_transform([pred])[0]
            st.success(f"Prediction: **{churn_label}**")
            if proba is not None:
                st.metric("Churn Probability", f"{proba:.2%}")
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
