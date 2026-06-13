from typing import Dict, Any
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pandas as pd
import joblib
from pathlib import Path


MODEL_DIR = Path(__file__).parent.parent / 'models'


def train_random_forest(X, y, cv: int = 5) -> Dict[str, Any]:
    param_grid = {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]}
    grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=cv, n_jobs=-1)
    grid.fit(X, y)
    best = grid.best_estimator_
    cv_scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    return {
        'model': best,
        'name': 'Random Forest',
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def train_logistic_regression(X, y, cv: int = 5) -> Dict[str, Any]:
    param_grid = {'C': [0.1, 1, 10], 'solver': ['liblinear', 'lbfgs']}
    grid = GridSearchCV(LogisticRegression(random_state=42, max_iter=1000), param_grid, cv=cv, n_jobs=-1)
    grid.fit(X, y)
    best = grid.best_estimator_
    cv_scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    return {
        'model': best,
        'name': 'Logistic Regression',
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def train_gradient_boosting(X, y, cv: int = 5) -> Dict[str, Any]:
    param_grid = {'n_estimators': [100, 200], 'learning_rate': [0.05, 0.1], 'max_depth': [3, 5]}
    grid = GridSearchCV(GradientBoostingClassifier(random_state=42), param_grid, cv=cv, n_jobs=-1)
    grid.fit(X, y)
    best = grid.best_estimator_
    cv_scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    return {
        'model': best,
        'name': 'Gradient Boosting',
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def train_svm(X, y, cv: int = 5) -> Dict[str, Any]:
    param_grid = {'C': [0.1, 1], 'kernel': ['linear', 'rbf']}
    grid = RandomizedSearchCV(SVC(random_state=42, probability=True), param_grid, cv=cv, n_jobs=-1, n_iter=4)
    grid.fit(X, y)
    best = grid.best_estimator_
    cv_scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    return {
        'model': best,
        'name': 'SVM',
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def train_knn(X, y, cv: int = 5) -> Dict[str, Any]:
    param_grid = {'n_neighbors': [3, 5, 7]}
    grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=cv, n_jobs=-1)
    grid.fit(X, y)
    best = grid.best_estimator_
    cv_scores = cross_val_score(best, X, y, cv=cv, scoring='accuracy')
    return {
        'model': best,
        'name': 'KNN',
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def train_all_models(X, y, cv: int = 5) -> Dict[str, Dict[str, Any]]:
    trainers = [
        train_random_forest,
        train_logistic_regression,
        train_gradient_boosting,
        train_svm,
        train_knn
    ]
    results = {}
    for trainer in trainers:
        result = trainer(X, y, cv=cv)
        results[result['name']] = result
    return results


def save_model(result: Dict[str, Any], filename: str):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(result, MODEL_DIR / filename)


def load_model(filename: str) -> Dict[str, Any]:
    return joblib.load(MODEL_DIR / filename)
