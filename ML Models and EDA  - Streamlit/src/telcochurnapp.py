import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from scipy.sparse import csr_matrix

# Streamlit page configuration
st.set_page_config(
    page_title="Telco Churn Prediction",
    page_icon="📞",
    layout="wide"
)

# Load the dataset
@st.cache_data
def load_data(file_path=None):
    if file_path:
        data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    else:
        data = pd.read_csv("C:\\Users\\MoseS\\Desktop\\telcochurn_project\\data\\CleanedTelco.csv")
    return data

# Preprocess the data
@st.cache_data
def preprocess_data(data):
    # Remove 'customerID' as it's not a predictive feature
    data = data.drop('customerID', axis=1, errors='ignore')
    
    # Separate features and target
    X = data.drop('Churn', axis=1)
    y = data['Churn']
    
    # Identify numeric and categorical columns
    numeric_columns = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = X.select_dtypes(include=['object']).columns
    
    # Handle numeric columns
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Handle categorical columns
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_columns),
            ('cat', categorical_transformer, categorical_columns)
        ])
    
    # Fit and transform the data
    X_processed = preprocessor.fit_transform(X)
    
    # Convert target to numeric
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    return X_processed, y, preprocessor

# Train multiple models and return the selected one
@st.cache_data
def train_models(_X, y):
    X = csr_matrix(_X) if isinstance(_X, csr_matrix) else _X
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Random Forest": RandomForestClassifier(random_state=42),
        "Logistic Regression": LogisticRegression(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        trained_models[name] = {"model": model, "accuracy": accuracy}
    
    return trained_models

# Preprocess user input for prediction
def preprocess_user_input(input_data, preprocessor):
    return preprocessor.transform(input_data)

# Main Streamlit app function
def main():
    st.markdown(
        "<h1 style='text-align: center; color: green; font-family: Arial Black;'>📞 TELCO CHURN</h1>",
        unsafe_allow_html=True,
    )
    
    menu_options = {
        "🏠 Home": home_page,
        "📊 Data": data_page,
        "📈 Dashboard": dashboard_page,
        "🔮 Predict": predict_page,
        "📜 History": history_page
    }
    
    choice = st.sidebar.selectbox("Navigation", list(menu_options.keys()))
    
    # Clear previous content
    st.empty()
    
    # Display the selected page
    menu_options[choice]()
    
    st.markdown(
        """
        <footer style='text-align: center; margin-top: 50px;'>
            Share on social media with the hashtag <b>#telcochurn</b>!<br>
            More info and ⭐ at <a href='#'>https://github.com/ndumbe0/Embedding-ML-Models-in-GUIs---Streamlit?tab=readme-ov-file#telco-churn-prediction-app</a>.
        </footer>
        """,
        unsafe_allow_html=True,
    )

def home_page():
    st.title("Welcome to Telco Churn Prediction App")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🔑 Key Features")
        st.write("- 🎯 Predict customer churn with high accuracy")
        st.write("- 📊 Analyze customer data to identify churn factors")
        st.write("- 📈 Visualize model performance and insights")
        
        st.header("🚀 How to Run the Application")
        st.write("1. 🧭 Navigate through the sidebar menu")
        st.write("2. 📁 Upload your data or use the sample dataset")
        st.write("3. 🤖 Train models and make predictions")
    
    with col2:
        st.header("🧠 Machine Learning Integration")
        st.write("- 🌳 Random Forest")
        st.write("- 📊 Logistic Regression")
        st.write("- 🚀 Gradient Boosting")
        st.write("- 🔄 Automated data preprocessing")
        st.write("- 🏆 Model performance comparison")
        
        st.header("💼 User Benefits")
        st.write("- 🔍 Identify at-risk customers before they churn")
        st.write("- 📈 Optimize retention strategies")
        st.write("- 😊 Improve customer satisfaction and loyalty")

def data_page():
    st.subheader("Dataset Overview")
    
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file:
        file_path = f"uploaded_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        data = load_data(file_path)
        st.success("File uploaded successfully!")
    else:
        data = load_data()
    
    st.dataframe(data)

def dashboard_page():
    st.subheader("Model Performance Dashboard")
    
    data = load_data()
    X, y, preprocessor = preprocess_data(data)
    trained_models = train_models(X, y)
    
    st.write("Accuracy of Trained Models:")
    for model_name, model_info in trained_models.items():
        st.markdown(f"**{model_name}:** {model_info['accuracy']:.2f}")

def predict_page():
    st.subheader("Predict Customer Churn")
    
    data = load_data()
    X, y, preprocessor = preprocess_data(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", options=["Male", "Female"])
        tenure = st.number_input("Tenure (in months)", min_value=0, max_value=200, step=1)

    with col2:
        internet_service = st.selectbox("Internet Service", options=["DSL", "Fiber optic", "No"])
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, step=0.01)
        total_charges = st.number_input("Total Charges", min_value=0.0, step=0.01)

    selected_model_name = st.selectbox("Select Machine Learning Model", options=["Random Forest", "Logistic Regression", "Gradient Boosting"])
    
    if st.button("Submit"):
        input_df = pd.DataFrame([{
            "gender": gender,
            "tenure": tenure,
            "InternetService": internet_service,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }])
        
        input_processed = preprocess_user_input(input_df, preprocessor)
        
        trained_models = train_models(X, y)
        selected_model = trained_models[selected_model_name]["model"]
        
        prediction = selected_model.predict(input_processed)[0]
        probability = selected_model.predict_proba(input_processed)[0][1]
        
        churn_status = "Yes" if prediction == 1 else "No"
        st.success(f"Prediction: Customer Churn is {churn_status}")
        st.write(f"**Probability of Churn:** {probability:.2f}")

def history_page():
    st.subheader("View Data History")
    
    data = load_data()
    st.dataframe(data)

if __name__ == "__main__":
    main()
