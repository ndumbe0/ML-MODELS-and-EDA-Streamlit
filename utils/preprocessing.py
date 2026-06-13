from typing import Tuple, List
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import csr_matrix


def preprocess_data(df: pd.DataFrame) -> Tuple[csr_matrix, np.ndarray, ColumnTransformer, LabelEncoder]:
    """Preprocess data with pipelines."""
    df = df.copy()
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

    X_processed = preprocessor.fit_transform(X)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X_processed, y_encoded, preprocessor, le
