from typing import Optional
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, r2_score


def plot_histogram(df: pd.DataFrame, column: str, title: Optional[str] = None):
    fig = px.histogram(df, x=column, marginal="box", nbins=30, title=title or f"{column} Distribution")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_boxplot(df: pd.DataFrame, x: str, y: str, title: Optional[str] = None):
    fig = px.box(df, x=x, y=y, color=x, title=title or f"{y} by {x}")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_correlation_heatmap(df: pd.DataFrame, columns: list, title: str = "Correlation Heatmap"):
    corr = df[columns].corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, aspect="auto", title=title)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_pairplot(df: pd.DataFrame, columns: list, color_col: str):
    fig = px.scatter_matrix(df[columns + [color_col]], dimensions=columns, color=color_col, height=800)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_churn_distribution(df: pd.DataFrame):
    fig = px.pie(df, names='Churn', title='Churn Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_missing_values(df: pd.DataFrame):
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        st.success("No missing values found.")
        return
    fig = px.bar(x=missing.index, y=missing.values, labels={'x': 'Column', 'y': 'Missing Count'}, title='Missing Values by Column')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_confusion_matrix(y_true, y_pred, labels: list = None):
    cm = confusion_matrix(y_true, y_pred)
    fig = px.imshow(cm, text_auto=True, labels=dict(x="Predicted", y="Actual"), x=labels, y=labels, title="Confusion Matrix")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_feature_importance(importance: np.ndarray, feature_names: list, title: str = "Feature Importance"):
    df_imp = pd.DataFrame({'Feature': feature_names, 'Importance': importance}).sort_values('Importance', ascending=True)
    fig = px.bar(df_imp, x='Importance', y='Feature', orientation='h', title=title)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
