# Telco Churn Analysis & Prediction Platform

![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-FA9F3E?logo=scikitlearn)
![Plotly](https://img.shields.io/badge/Plotly-6.8-3F4F75?logo=plotly)

![Telco Churn Dashboard](https://github.com/user-attachments/assets/4dafda63-22b6-4d15-8c1b-dbd3b1f45697)

An end-to-end machine learning platform for telecommunications customer churn analysis and prediction. Built with Streamlit, this application combines interactive exploratory data analysis (EDA), automated ML model training with hyperparameter tuning, and an AI-powered assistant for insights.

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [ML Models](#ml-models)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Overview

Customer churn is one of the most critical metrics for subscription-based businesses. This platform enables data scientists and business analysts to:

1. **Explore** customer data with interactive visualizations
2. **Train and compare** multiple ML models with cross-validation
3. **Predict** individual customer churn probability
4. **Get AI-powered insights** via integrated Gemini AI assistant

## Live Demo

![Dashboard Preview](https://github.com/user-attachments/assets/6510f5bf-9b24-48c6-9b7b-e9637ca1cadd)

**Live App:** [Telco Churn Platform](https://ndumbe0-embedding-ml-models-in-guis---streamli-srcedaapp-bpzjl8.streamlit.app/)

## Features

### Data & EDA
- **Upload** CSV/Excel datasets or use built-in Telco data
- **Interactive plots** using Plotly: histograms, boxplots, scatter matrices, correlation heatmaps
- **Missing value analysis** and class distribution charts
- **Automated data cleaning** and preprocessing pipelines

### Machine Learning
- **5 algorithms** trained and compared: Random Forest, Logistic Regression, Gradient Boosting, SVM, KNN
- **Cross-validation** with configurable folds
- **Hyperparameter tuning** via GridSearchCV / RandomizedSearchCV
- **Model leaderboard** with accuracy, precision, recall, F1 scores
- **Feature importance** visualizations
- **Confusion matrices** and regression error plots
- **Model persistence** with joblib for fast reloading

### User Interface
- **Multi-page navigation**: Home, EDA, Model Training, Prediction, About
- **Download buttons** for cleaned datasets, predictions, and plots
- **Responsive layout** with sidebar controls and filters
- **Loading spinners** and status messages

### AI Assistant
- **Gemini AI integration** via Google Generative AI SDK
- Ask questions about EDA findings or model results
- Secure API key management via `.env` files

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.11+ |
| **Web Framework** | Streamlit 1.58 |
| **ML** | scikit-learn, pandas, numpy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **AI** | Google Generative AI (Gemini) |
| **DevOps** | Docker, Docker Compose |

## Project Structure

```
ML-MODELS-and-EDA-Streamlit/
├── app.py                 # Main application entry point
├── pages/
│   ├── Home.py           # Welcome page with metrics
│   ├── EDA.py            # Exploratory data analysis
│   ├── Model_Training.py # Model comparison and tuning
│   ├── Prediction.py     # Customer churn prediction
│   └── About.py          # Project information
├── utils/
│   ├── data_loader.py    # Data loading and cleaning
│   ├── preprocessing.py  # sklearn Pipelines
│   └── visualizations.py # Plotly chart generators
├── models/
│   └── trainer.py        # ML model training logic
├── data/
│   └── CleanedTelco.csv  # Default dataset
├── images/               # README assets
├── Dockerfile            # Container definition
├── docker-compose.yml    # Multi-service orchestration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── .gitignore
```

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ndumbe0/ML-MODELS-and-EDA-Streamlit.git
   cd ML-MODELS-and-EDA-Streamlit
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open browser** to `http://localhost:8501`

## Docker Deployment

Run the entire application in a container:

```bash
docker-compose up --build
```

Then visit `http://localhost:8501`.

### Docker Options

**Build only:**
```bash
docker build -t telco-churn-app .
```

**Run container:**
```bash
docker run -p 8501:8501 -e GOOGLE_AI_API_KEY=your_key telco-churn-app
```

## ML Models

The application trains and compares 5 machine learning models:

| Model | Algorithm | Hyperparameter Tuning |
|-------|-----------|----------------------|
| **Random Forest** | `RandomForestClassifier` | GridSearchCV |
| **Logistic Regression** | `LogisticRegression` | GridSearchCV |
| **Gradient Boosting** | `GradientBoostingClassifier` | GridSearchCV |
| **SVM** | `SVC` | RandomizedSearchCV |
| **KNN** | `KNeighborsClassifier` | GridSearchCV |

### Model Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Numeric pipeline
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combined preprocessor
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_cols),
    ('cat', categorical_transformer, categorical_cols)
])
```

## Screenshots

### Home Page
![Home](https://github.com/user-attachments/assets/eda1example)

### EDA Dashboard
![EDA Dashboard](https://github.com/user-attachments/assets/eda2example)

### Model Training
![Model Training](https://github.com/user-attachments/assets/eda1-1example)

### Prediction Interface
![Prediction](https://github.com/user-attachments/assets/loginexample)

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_AI_API_KEY=your_google_generative_ai_api_key
```

> **Note:** Never commit `.env` files. Use `.env.example` as a template.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Developer

**Moses N Ndumbe**  
**Team Lead:** Ms. Portia Bentum  
**Organization:** Azubi Africa

---

Built with passion for data science and machine learning.

![GitHub stars](https://img.shields.io/github/stars/ndumbe0/ML-MODELS-and-EDA-Streamlit?style=social)
