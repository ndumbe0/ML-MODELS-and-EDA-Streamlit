# Install required packages before running: streamlit, pandas, matplotlib, seaborn, plotly
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Authentication setup
def authenticate(username, password):
    valid_users = {"admin": "password123", "user": "userpass"}
    return valid_users.get(username) == password

# Load datasets
@st.cache_data
def load_data():
    # Replace with your file paths or database connections
    df_train = pd.read_csv("Exploratory-Analysis.csv")  # Replace with actual file path
    df_test = pd.read_csv("testcleaned.csv")  # Replace with actual file path
    return df_train, df_test

# Streamlit app starts here
st.set_page_config(page_title="EDA & Analytics Dashboard", layout="wide")

# Authentication form
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if not authenticate(username, password):
    st.sidebar.error("Invalid username or password.")
    st.stop()

# Load data
df_train, df_test = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["EDA Dashboard", "Analytics Dashboard"])

if page == "EDA Dashboard":
    st.title("Exploratory Data Analysis (EDA) Dashboard")

    # Dataset selection
    dataset_choice = st.selectbox("Select Dataset", ["Training Data", "Test Data"])
    df = df_train if dataset_choice == "Training Data" else df_test

    # Interactive visualizations
    st.subheader("Visualizations")

    # Histogram of Monthly Charges
    st.write("### Monthly Charges Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["MonthlyCharges"], bins=30, kde=True, ax=ax)
    ax.set_title("Monthly Charges Distribution")
    st.pyplot(fig)

    # Boxplot of Monthly Charges by Churn
    st.write("### Monthly Charges by Churn")
    fig, ax = plt.subplots()
    sns.boxplot(x="Churn", y="MonthlyCharges", data=df, ax=ax)
    ax.set_title("Monthly Charges by Churn")
    st.pyplot(fig)

    # Scatter plot of Total Charges vs. Monthly Charges colored by Churn
    if "TotalCharges" in df.columns:
        st.write("### Total Charges vs. Monthly Charges (Colored by Churn)")
        fig = px.scatter(df, x="MonthlyCharges", y="TotalCharges", color="Churn",
                         title="Total Charges vs. Monthly Charges")
        st.plotly_chart(fig)

elif page == "Analytics Dashboard":
    st.title("Analytics Dashboard")

    # Dataset selection for KPIs
    dataset_choice = st.selectbox("Select Dataset for KPIs", ["Training Data", "Test Data"])
    df = df_train if dataset_choice == "Training Data" else df_test

    # Key Performance Indicators (KPIs)
    st.subheader("Key Metrics")
    
    total_customers = len(df)
    churned_customers = len(df[df["Churn"] == "Yes"])
    churn_rate = churned_customers / total_customers * 100
    
    avg_monthly_charges = df["MonthlyCharges"].mean()
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Customers", total_customers)
    col2.metric("Churned Customers", churned_customers)
    col3.metric("Churn Rate (%)", f"{churn_rate:.2f}")
    
    col1.metric("Average Monthly Charges ($)", f"{avg_monthly_charges:.2f}")
    
    if "TotalCharges" in df.columns:
        avg_total_charges = df["TotalCharges"].mean()
        col2.metric("Average Total Charges ($)", f"{avg_total_charges:.2f}")

# Footer personalization
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: gray;'>© 2025 EDA & Analytics Dashboard</h5>", unsafe_allow_html=True)
