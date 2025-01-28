import streamlit as st
import yaml
from yaml.loader import SafeLoader

# Configuration and styling
st.set_page_config(page_title="Stylish Auth App", page_icon="🔐", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #4CAF50;
        padding: 10px;
    }
    .css-1cpxqw2 {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create an authentication object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Main app
def main():
    st.title("🔐 Stylish Auth App")
    
    # Authentication status
    name, authentication_status, username = authenticator.login("Login", "main")
    
    if authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")
    elif authentication_status:
        # Successful login
        st.success(f"Welcome, {name}!")
        st.balloons()
        
        # Logout button
        authenticator.logout("Logout", "sidebar")
        
        # Main content after login
        st.header("Dashboard")
        st.write("This is your personalized dashboard. Enjoy your stay!")
        
        # Sample interactive element
        if st.button("Click me for a surprise!"):
            st.snow()
    
    # Reset password button
    if st.button("Reset Password"):
        try:
            if authenticator.reset_password(username, "Reset password"):
                st.success("Password modified successfully")
        except Exception as e:
            st.error(e)
    
    # Help link
    st.link_button("Need Help?", "https://example.com/help", type="secondary")

if __name__ == "__main__":
    main()
