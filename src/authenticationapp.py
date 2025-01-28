import streamlit as st
import time

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    body {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #e0e6ed 0%, #8b9dc9 50%, #9b8da8 100%);
    }
    
    .login-container {
        max-width: 320px !important;
        margin: 20px auto 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .login-header {
        text-align: center;
    margin-bottom: 1.5rem;
    color: #000000;
    font-size: 22px;
    font-weight: 600;
    }
    
    .login-icon {
        width: 48px;
        height: 48px;
        margin: 0 auto 15px auto;
        display: block;
    }
    
    .stTextInput label {
        color: #4a5568 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        padding: 8px 12px;
        border-radius: 8px;
        height: 38px;
        font-size: 14px;
        color: #2d3748;
        font-weight: 400;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4299e1;
        box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4299e1 0%, #667eea 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 15px;
        width: 100%;
        height: 38px;
        font-size: 14px;
        font-weight: 500;
        margin: 10px 0;
        transition: transform 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    .auth-links, .divider-text {
        color: #4a5568 !important;
        font-weight: 400 !important;
        font-size: 13px !important;
        text-align: center;
    }
    
    .auth-links a, .forgot-link {
        color: #4299e1 !important;
        font-weight: 500 !important;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
    }
    
    .social-icon {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        padding: 8px;
        background: #f7fafc;
        transition: transform 0.2s ease, background 0.2s ease;
    }
    
    .social-icon:hover {
        transform: translateY(-2px);
        background: #edf2f7;
    }
</style>
""", unsafe_allow_html=True)

def login_form():
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Updated login icon with a modern design
        st.markdown("""
            <div style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/6681/6681204.png" 
                     class="login-icon">
                <h1 class="login-header">Welcome Back</h1>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown('<div style="text-align: right; margin: -5px 0 10px;"><a href="#" class="forgot-link" onclick="alert(\'Reset password functionality\')">Forgot password?</a></div>', unsafe_allow_html=True)
        
        login_button = st.button("Sign In")
        
        if login_button:
            with st.spinner('Authenticating...'):
                time.sleep(1)
                if username == "admin" and password == "admin123":
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid credentials")
        
        st.markdown('<div class="divider-text">Or continue with</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="social-icons">
                <img src="https://cdn-icons-png.flaticon.com/512/5968/5968764.png" class="social-icon" alt="Facebook" onclick="alert('Facebook login')">
                <img src="https://cdn-icons-png.flaticon.com/512/3670/3670151.png" class="social-icon" alt="Twitter" onclick="alert('Twitter login')">
                <img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" class="social-icon" alt="Google" onclick="alert('Google login')">
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-links">
                New user? <a href="#" onclick="alert('Sign up functionality')">Create account</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_form()
    else:
        st.write("Welcome to the application!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
