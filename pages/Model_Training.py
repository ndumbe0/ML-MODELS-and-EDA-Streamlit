import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from models.trainer import train_all_models
from utils.visualizations import plot_confusion_matrix, plot_feature_importance


def show():
    st.title("Model Training & Comparison")
    uploaded_file = st.sidebar.file_uploader("Upload dataset", type=['csv', 'xlsx'], key="train_upload")
    df = load_data(uploaded_file=uploaded_file)
    if df is None:
        return

    cv_folds = st.sidebar.slider("Cross-Validation Folds", 2, 10, 5)
    test_size = st.sidebar.slider("Test Set Size", 0.1, 0.4, 0.2)

    X, y, preprocessor, le = preprocess_data(df)

    if st.button("Train All Models", type="primary"):
        with st.spinner("Training models with cross-validation and hyperparameter tuning..."):
            results = train_all_models(X, y, cv=cv_folds)
            st.session_state['model_results'] = results
            st.session_state['preprocessor'] = preprocessor
            st.session_state['label_encoder'] = le
            st.success("Training complete!")

    if 'model_results' in st.session_state:
        results = st.session_state['model_results']
        leaderboard = pd.DataFrame([{
            'Model': r['name'],
            'Best CV Score': r['best_score'],
            'CV Mean': r['cv_mean'],
            'CV Std': r['cv_std'],
            'Best Params': str(r['best_params'])
        } for r in results.values()])
        st.subheader("Model Leaderboard")
        st.dataframe(leaderboard.sort_values('Best CV Score', ascending=False), use_container_width=True)

        fig = px.bar(leaderboard, x='Model', y='Best CV Score', color='Model', title="Model Comparison")
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

        selected_model = st.selectbox("Select model for details", list(results.keys()))
        res = results[selected_model]
        st.write(f"**Best Parameters:** {res['best_params']}")

        if hasattr(res['model'], 'feature_importances_'):
            try:
                feature_names = list(res['model'].feature_names_in_)
            except AttributeError:
                feature_names = [f"Feature {i}" for i in range(len(res['model'].feature_importances_))]
            plot_feature_importance(res['model'].feature_importances_, feature_names, f"{selected_model} Feature Importance")
