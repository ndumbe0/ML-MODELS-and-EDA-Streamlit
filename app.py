import os
import logging
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from pages import Home, EDA, Model_Training, Prediction, About
from utils.data_loader import load_data
from utils.visualizations import plot_confusion_matrix

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Telco Churn ML Platform", page_icon="📊", layout="wide")

with st.sidebar:
    st.title("Telco ML Platform")
    st.markdown("---")
    page = st.radio("Navigation", ["Home", "EDA", "Model Training", "Prediction", "About"])
    st.markdown("---")
    st.subheader("Settings")
    show_gemini = st.checkbox("Show AI Assistant", value=True)
    st.markdown("---")
    st.caption("Upload a dataset in any page to get started.")

st.sidebar.markdown("---")
st.sidebar.caption("Upload a dataset in any page to get started.")

for key in ['model_results', 'preprocessor', 'label_encoder']:
    if key not in st.session_state:
        st.session_state[key] = None

def _sanitize_prompt_input(text, max_len=2000):
    if not text or not isinstance(text, str):
        return ""
    text = text.strip()[:max_len]
    forbidden = [
        "ignore previous instructions", "ignore all instructions",
        "ignore all previous", "you are now", "act as", "system prompt",
        "forget everything", "override", "you are a",
    ]
    lower = text.lower()
    for pattern in forbidden:
        if pattern in lower:
            text = text.replace(pattern, "[redacted]")
    return text


try:
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
except Exception as e:
    st.error(f"Page error: {str(e)}")
    logger.error(f"Error rendering page '{page}': {e}")

if show_gemini and 'GOOGLE_API_KEY' in os.environ:
    st.markdown("---")
    with st.expander("🤖 Gemini AI Assistant", expanded=False):
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-2.0-flash')
        user_q = st.text_input("Ask about the data, models, or results:")
        if user_q:
            sanitized_q = _sanitize_prompt_input(user_q)
            if not sanitized_q:
                st.warning("Invalid or empty input.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        response = model.generate_content(sanitized_q)
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI error: {str(e)}")
