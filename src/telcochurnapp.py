import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Streamlit page configuration with a telephone icon and churn sign
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
    # Clean column names
    data.columns = data.columns.str.strip()
    
    # Ensure required columns exist
    required_columns = ['customerID', 'Churn', 'InternetService']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"Required column '{col}' is missing from the dataset.")
    
    # Define mappings for categorical columns
    mappings = {
        'gender': {'Male': 0, 'Female': 1},
        'Partner': {'No': 0, 'Yes': 1},
        'Dependents': {'No': 0, 'Yes': 1},
        'Churn': {'No': 0, 'Yes': 1},
        'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2}
    }
    
    # Apply mappings to relevant columns
    for column, mapping in mappings.items():
        if column in data.columns:
            data[column] = data[column].map(mapping)
    
    # One-hot encode remaining categorical variables
    data = pd.get_dummies(data, drop_first=True)
    
    # Handle missing values (if any)
    data.fillna(0, inplace=True)
    
    # Select features and target variable
    X = data.drop(columns=['customerID', 'Churn'], errors='ignore')
    y = data['Churn']
    
    return X, y

# Train multiple models and return the selected one
@st.cache_data
def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        trained_models[name] = {"model": model, "accuracy": accuracy}
    
    return trained_models

# Preprocess user input for prediction
def preprocess_user_input(input_data, feature_columns):
    mappings = {
        'gender': {'Male': 0, 'Female': 1},
        'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2}
    }
    
    for column, mapping in mappings.items():
        if column in input_data.columns:
            input_data[column] = input_data[column].map(mapping)
    
    input_data = pd.get_dummies(input_data, drop_first=True)
    
    aligned_input_df = pd.DataFrame(columns=feature_columns).combine_first(input_data).fillna(0)
    
    return aligned_input_df[feature_columns]  # Ensure column order matches training features

# Main Streamlit app function
def main():
    # Header with fancy font and central alignment
    st.markdown(
        "<h1 style='text-align: center; color: green; font-family: Arial Black;'>TELCO CHURN</h1>",
        unsafe_allow_html=True,
    )
    
    try:
        # Sidebar Navigation Panel with gradient color theme and icons for each section
        st.sidebar.markdown(
            """
            <style>
                .sidebar .sidebar-content { background-color: #f8f9fa; }
                .nav-link:hover { background-color: #e9ecef; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        menu_options = {
            "📊 Data": "data",
            "📈 Dashboard": "dashboard",
            "🔮 Predict": "predict",
            "📜 History": "history"
        }
        
        menu_choice = st.sidebar.radio("Navigation", list(menu_options.keys()))
        
        if menu_options[menu_choice] == "data":
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

        elif menu_options[menu_choice] == "dashboard":
            st.subheader("Model Performance Dashboard")
            
            data = load_data()
            X, y = preprocess_data(data)
            trained_models = train_models(X, y)
            
            st.write("Accuracy of Trained Models:")
            for model_name in trained_models.keys():
                st.markdown(f"**{model_name}:** {trained_models[model_name]['accuracy']:.2f}")

        elif menu_options[menu_choice] == "predict":
            st.subheader("Predict Customer Churn")
            
            col1, col2 = st.columns(2)
            
            with col1:
                customer_id = st.text_input("Customer ID")
                gender = st.selectbox("Gender", options=["Male", "Female"])
                tenure = st.slider("Tenure (in months)", min_value=0, max_value=200)

            with col2:
                internet_service = st.selectbox("Internet Service", options=["DSL", "Fiber optic", "No"])
                monthly_charges = st.number_input("Monthly Charges", min_value=0.0)
                total_charges = st.number_input("Total Charges", min_value=0.0)

            selected_model_name = st.selectbox("Select Machine Learning Model", options=["Random Forest", "Logistic Regression", "Gradient Boosting"])
            
            if st.button("Submit"):
                input_df = pd.DataFrame([{
                    "customerID": customer_id,
                    "gender": gender,
                    "tenure": tenure,
                    "InternetService": internet_service,
                    "MonthlyCharges": monthly_charges,
                    "TotalCharges": total_charges,
                }])
                
                data = load_data()
                X, _ = preprocess_data(data)
                
                input_df_preprocessed = preprocess_user_input(input_df, X.columns)
                
                trained_models = train_models(X, _)
                selected_model = trained_models[selected_model_name]["model"]
                
                prediction = selected_model.predict(input_df_preprocessed)[0]
                probability = selected_model.predict_proba(input_df_preprocessed)[0][1]
                
                churn_status = "Yes" if prediction == 1 else "No"
                st.success(f"Prediction: Customer Churn is {churn_status}")
                st.write(f"**Probability of Churn:** {probability:.2f}")
        
        elif menu_options[menu_choice] == "history":
            st.subheader("View Data History")
            
            data = load_data()
            st.dataframe(data)

        # Add footer with social sharing option and repository link placeholder.
        st.markdown(
            """
            <footer style='text-align: center; margin-top: 50px;'>
                Share on social media with the hashtag <b>#telcochurn</b>!<br>
                More info and ⭐ at <a href='#'>GitHub Repository</a>.
            </footer>
            """,
            unsafe_allow_html=True,
        )

    except KeyError as e:
        st.error(f"KeyError: {e}. Please check your dataset.")
        
if __name__ == "__main__":
    main()
