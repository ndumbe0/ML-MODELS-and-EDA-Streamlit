import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load datasets
@st.cache_data
def load_data():
    try:
        df_train = pd.read_csv("C:\\Users\\MoseS\\Desktop\\telcochurn_project\\data\\telcocleaned.csv")
        df_test = pd.read_csv("C:\\Users\\MoseS\\Desktop\\telcochurn_project\\data\\testcleaned.csv")
    except FileNotFoundError:
        st.error("CSV files not found. Please check the file paths.")
        return None, None
    
    def clean_dataframe(df):
        # Convert 'TotalCharges' to numeric, replacing any non-convertible values with NaN
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        
        # Drop rows with NaN values in 'TotalCharges'
        df = df.dropna(subset=['TotalCharges'])
        
        # Convert all columns to string type
        df = df.astype(str)
        
        return df
    
    df_train = clean_dataframe(df_train)
    df_test = clean_dataframe(df_test)
    
    return df_train, df_test

# Streamlit app starts here
st.set_page_config(page_title="Telco Churn Analysis Dashboard", layout="wide")

# Load data
df_train, df_test = load_data()

if df_train is None or df_test is None:
    st.stop()

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
    sns.histplot(df["MonthlyCharges"].astype(float), bins=30, kde=True, ax=ax)
    ax.set_title("Monthly Charges Distribution")
    st.pyplot(fig)

    # Boxplot of Monthly Charges by Churn
    st.write("### Monthly Charges by Churn")
    fig, ax = plt.subplots()
    sns.boxplot(x="Churn", y="MonthlyCharges", data=df.astype({'MonthlyCharges': 'float64'}), ax=ax)
    ax.set_title("Monthly Charges by Churn")
    st.pyplot(fig)

    # Scatter plot of Total Charges vs. Monthly Charges colored by Churn
    st.write("### Total Charges vs. Monthly Charges (Colored by Churn)")
    fig = px.scatter(df.astype({'MonthlyCharges': 'float64', 'TotalCharges': 'float64'}), 
                     x="MonthlyCharges", y="TotalCharges", color="Churn",
                     title="Total Charges vs. Monthly Charges")
    st.plotly_chart(fig)

    # Correlation heatmap
    st.write("### Correlation Heatmap")
    numeric_cols = ['MonthlyCharges', 'TotalCharges']
    corr_matrix = df[numeric_cols].astype(float).corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

    # Churn distribution
    st.write("### Churn Distribution")
    fig, ax = plt.subplots()
    df['Churn'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title("Churn Distribution")
    st.pyplot(fig)

elif page == "Analytics Dashboard":
    st.title("Analytics Dashboard")

    # Dataset selection for KPIs
    dataset_choice = st.selectbox("Select Dataset for KPIs", ["Training Data", "Test Data"])
    df = df_train if dataset_choice == "Training Data" else df_test

    # Key Performance Indicators (KPIs)
    st.subheader("Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    # Total Customers
    total_customers = len(df)
    col1.metric("Total Customers", f"{total_customers:,}")
    
    # Churned Customers
    churned_customers = len(df[df["Churn"] == "Yes"])
    col2.metric("Churned Customers", f"{churned_customers:,}")
    
    # Churn Rate
    churn_rate = churned_customers / total_customers * 100
    col3.metric("Churn Rate (%)", f"{churn_rate:.2f}")
    
    # Average Monthly Charges
    avg_monthly_charges = df["MonthlyCharges"].astype(float).mean()
    col1.metric("Average Monthly Charges ($)", f"{avg_monthly_charges:.2f}")
    
    # Average Total Charges
    avg_total_charges = df["TotalCharges"].astype(float).mean()
    col2.metric("Average Total Charges ($)", f"{avg_total_charges:.2f}")

    # Churn by Contract Type
    st.subheader("Churn by Contract Type")
    contract_churn = df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack()
    fig = px.bar(contract_churn, x=contract_churn.index, y=["Yes", "No"], 
                 title="Churn Rate by Contract Type", barmode="group")
    st.plotly_chart(fig)

    # Top 5 Reasons for Churn
    st.subheader("Top 5 Reasons for Churn")
    churn_reasons = df[df["Churn"] == "Yes"].groupby("Contract").size().sort_values(ascending=False).head()
    fig = px.pie(values=churn_reasons.values, names=churn_reasons.index, 
                 title="Top 5 Reasons for Churn")
    st.plotly_chart(fig)

# Footer personalization
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: gray;'>© 2025 Telco Churn Analysis Dashboard</h5>", unsafe_allow_html=True)
