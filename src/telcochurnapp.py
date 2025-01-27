import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import smtplib
from email.mime.text import MIMEText
import webbrowser
import os
import threading

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
    # Remove 'customerID' column and other non-numeric columns
    X = data.drop(['Churn', 'customerID'], axis=1)
    # Convert categorical variables to numeric
    X = pd.get_dummies(X, drop_first=True)
    y = data['Churn']
    return X, y

# Train multiple models and return the selected one
@st.cache_data
def train_models(X, y):
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
def preprocess_user_input(input_data, feature_columns):
    # Convert categorical variables to numeric
    input_data_encoded = pd.get_dummies(input_data.drop('customerID', axis=1), drop_first=True)
    
    # Align input data with feature columns
    for col in feature_columns:
        if col not in input_data_encoded.columns:
            input_data_encoded[col] = 0
    
    return input_data_encoded[feature_columns]

# Send email function
def send_email(user_email, issue):
    sender_email = "your_email@gmail.com"  # Replace with your email
    password = "your_password"  # Replace with your email password
    
    msg = MIMEText(f"User Email: {user_email}\nIssue: {issue}")
    msg['Subject'] = "Help Request from Telco Churn App"
    msg['From'] = sender_email
    msg['To'] = "ndumbemoses@gmail.com"
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, password)
            smtp_server.sendmail(sender_email, "ndumbemoses@gmail.com", msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Home page function
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
    
    # Need Help button
    if st.button("Need Help? 🆘"):
        st.subheader("Contact Us")
        user_email = st.text_input("Your Email")
        issue = st.text_area("Describe your issue")
        if st.button("Send"):
            if send_email(user_email, issue):
                st.success("Your message has been sent. We'll get back to you soon!")
            else:
                st.error("Failed to send the message. Please try again later.")

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
    X, y = preprocess_data(data)
    trained_models = train_models(X, y)
    
    st.write("Accuracy of Trained Models:")
    for model_name, model_info in trained_models.items():
        st.markdown(f"**{model_name}:** {model_info['accuracy']:.2f}")

def predict_page():
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

def history_page():
    st.subheader("View Data History")
    
    data = load_data()
    st.dataframe(data)

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

if __name__ == "__main__":
    main()
