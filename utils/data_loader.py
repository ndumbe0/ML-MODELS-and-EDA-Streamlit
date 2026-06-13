import streamlit as st
import pandas as pd
import os
from typing import Optional, Tuple
from pathlib import Path


@st.cache_data
def load_data(file_path: Optional[str] = None, uploaded_file=None) -> Optional[pd.DataFrame]:
    """Load dataset from file path or uploaded file."""
    try:
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Use CSV or Excel.")
                return None
        elif file_path and Path(file_path).exists():
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        else:
            default_path = Path(__file__).parent.parent / 'data' / 'CleanedTelco.csv'
            if default_path.exists():
                df = pd.read_csv(default_path)
            else:
                st.error("Default dataset not found. Please upload a file.")
                return None
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df = df.dropna(subset=['TotalCharges'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the dataset."""
    df = df.copy()
    df = df.drop('customerID', axis=1, errors='ignore')
    return df


def get_feature_target_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate features and target variable."""
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    return X, y
