import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Telco Churn Analysis Dashboard", layout="wide")

# Custom CSS for animations
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.fade-in {
    animation: fadeIn 1s ease-out;
}
@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
.slide-in {
    animation: slideIn 1s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Load datasets
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df = df.dropna(subset=['TotalCharges'])
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["EDA Dashboard", "Analytics Dashboard"])

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your churn dataset (CSV or Excel)", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is None:
        st.stop()
else:
    st.warning("Please upload a dataset to begin analysis.")
    st.stop()

if page == "EDA Dashboard":
    st.markdown("<h1 class='fade-in'>Exploratory Data Analysis (EDA) Dashboard</h1>", unsafe_allow_html=True)

    # Interactive visualizations
    st.markdown("<h2 class='slide-in'>Visualizations</h2>", unsafe_allow_html=True)

    # Monthly Charges Distribution
    st.markdown("<h3 class='fade-in'>Monthly Charges Distribution</h3>", unsafe_allow_html=True)
    fig = px.histogram(df, x="MonthlyCharges", nbins=30, marginal="box")
    fig.update_layout(title_text="Monthly Charges Distribution", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Monthly Charges by Churn
    st.markdown("<h3 class='fade-in'>Monthly Charges by Churn</h3>", unsafe_allow_html=True)
    fig = px.box(df, x="Churn", y="MonthlyCharges", color="Churn")
    fig.update_layout(title_text="Monthly Charges by Churn", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Total Charges vs. Monthly Charges
    st.markdown("<h3 class='fade-in'>Total Charges vs. Monthly Charges</h3>", unsafe_allow_html=True)
    fig = px.scatter(df, x="MonthlyCharges", y="TotalCharges", color="Churn", 
                     hover_data=["Contract", "tenure"])
    fig.update_layout(title_text="Total Charges vs. Monthly Charges", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.markdown("<h3 class='fade-in'>Correlation Heatmap</h3>", unsafe_allow_html=True)
    numeric_cols = ['MonthlyCharges', 'TotalCharges', 'tenure']
    corr_matrix = df[numeric_cols].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
    fig.update_layout(title_text="Correlation Heatmap", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Churn distribution
    st.markdown("<h3 class='fade-in'>Churn Distribution</h3>", unsafe_allow_html=True)
    fig = px.pie(df, names='Churn', title='Churn Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Analytics Dashboard":
    st.markdown("<h1 class='fade-in'>Analytics Dashboard</h1>", unsafe_allow_html=True)

    # Key Performance Indicators (KPIs)
    st.markdown("<h2 class='slide-in'>Key Metrics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Animated counters for KPIs
    total_customers = len(df)
    churned_customers = len(df[df["Churn"] == "Yes"])
    churn_rate = churned_customers / total_customers * 100
    avg_monthly_charges = df["MonthlyCharges"].mean()
    avg_total_charges = df["TotalCharges"].mean()

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churned Customers", f"{churned_customers:,}")
    col3.metric("Churn Rate (%)", f"{churn_rate:.2f}")
    col1.metric("Avg Monthly Charges ($)", f"{avg_monthly_charges:.2f}")
    col2.metric("Avg Total Charges ($)", f"{avg_total_charges:.2f}")

    # Churn by Contract Type
    st.markdown("<h3 class='fade-in'>Churn by Contract Type</h3>", unsafe_allow_html=True)
    contract_churn = df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack()
    fig = px.bar(contract_churn, x=contract_churn.index, y=["Yes", "No"], 
                 title="Churn Rate by Contract Type", barmode="group")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 Reasons for Churn
    st.markdown("<h3 class='fade-in'>Top 5 Reasons for Churn</h3>", unsafe_allow_html=True)
    churn_reasons = df[df["Churn"] == "Yes"].groupby("Contract").size().sort_values(ascending=False).head()
    fig = px.pie(values=churn_reasons.values, names=churn_reasons.index, 
                 title="Top 5 Reasons for Churn")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Churn Rate Over Time
    st.markdown("<h3 class='fade-in'>Churn Rate Over Time</h3>", unsafe_allow_html=True)
    churn_over_time = df.groupby('tenure')['Churn'].apply(lambda x: (x == 'Yes').mean()).reset_index()
    churn_over_time.columns = ['tenure', 'ChurnRate']
    fig = px.line(churn_over_time, x='tenure', y='ChurnRate', title='Churn Rate Over Time')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Interactive Churn Predictor
    st.markdown("<h3 class='fade-in'>Interactive Churn Predictor</h3>", unsafe_allow_html=True)
    st.write("Adjust the sliders to see how different factors affect churn probability.")
    
    monthly_charges = st.slider("Monthly Charges ($)", 0, 200, 50)
    total_charges = st.slider("Total Charges ($)", 0, 10000, 2000)
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    
    # This is a simplified model for demonstration purposes
    churn_probability = (monthly_charges / 200 + total_charges / 10000 + (72 - tenure) / 72) / 3
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = churn_probability,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Churn Probability"},
        gauge = {'axis': {'range': [None, 1]},
                 'steps' : [
                     {'range': [0, 0.5], 'color': "lightgreen"},
                     {'range': [0.5, 0.75], 'color': "yellow"},
                     {'range': [0.75, 1], 'color': "red"}],
                 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.75}}))
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: gray;'>© 2025 Telco Churn Analysis Dashboard</h5>", unsafe_allow_html=True)
