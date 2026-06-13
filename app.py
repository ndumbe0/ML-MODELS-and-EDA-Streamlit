import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from pages import Home, EDA, Model_Training, Prediction, About
from utils.data_loader import load_data
from utils.visualizations import plot_confusion_matrix

st.set_page_config(page_title="Telco Churn ML Platform", page_icon="📊", layout="wide")

load_dotenv()

with st.sidebar:
    st.title("Telco ML Platform")
    st.markdown("---")
    page = st.radio("Navigation", ["Home", "EDA", "Model Training", "Prediction", "About"])
    st.markdown("---")
    st.subheader("Settings")
    show_gemini = st.checkbox("Show AI Assistant", value=True)
    st.markdown("---")
    st.caption("Upload a dataset in any page to get started.")

df_global = None
for key in ['model_results', 'preprocessor', 'label_encoder']:
    if key not in st.session_state:
        st.session_state[key] = None

if page == "Home":
    Home.show()
elif page == "EDA":
    EDA.show()
elif page == "Model Training":
    Model_Training.show()
elif page == "Prediction":
    Prediction.show()
elif page == "About":
    About.show()

if show_gemini and 'GOOGLE_API_KEY' in os.environ:
    st.markdown("---")
    with st.expander("🤖 Gemini AI Assistant", expanded=False):
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-2.0-flash')
        user_q = st.text_input("Ask about the data, models, or results:")
        if user_q:
            with st.spinner("Thinking..."):
                try:
                    response = model.generate_content(user_q)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI error: {str(e)}")
