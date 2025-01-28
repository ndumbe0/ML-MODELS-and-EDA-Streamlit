# Custom CSS with improved styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-container {
        max-width: 360px !important;
        margin: 50px auto 0 auto;  /* Reduced top margin */
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 1.5rem;
        color: #000000;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Input field labels */
    .stTextInput label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #eaecef;
        padding: 8px 12px;
        border-radius: 8px;
        height: 40px;
        font-size: 14px;
        color: #000000;
        font-weight: 500;
        width: 100%;
        max-width: 300px;
    }
    
    /* Login button */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 15px;
        width: 120px;
        height: 40px;
        font-size: 14px;
        font-weight: 700;
        margin: auto;
        display: block;
    }
    
    /* Links and text */
    .auth-links, .divider-text {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    .auth-links a, .forgot-link {
        color: #000000 !important;
        font-weight: 700 !important;
        text-decoration: none;
    }
    
    /* Social login section */
    .social-section {
        margin-top: 20px;
        text-align: center;
    }
    
    .social-text {
        color: #000000;
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 10px;
    }
    
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 10px;
    }
    
    .social-icon {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        padding: 5px;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Modified HTML for the login form
def login_form():
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Avatar and title with reduced spacing
        st.markdown("""
            <div style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" 
                     style="width: 60px; height: 60px; margin-bottom: 10px;">
                <h1 class="login-header">Login</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Login form with bold labels
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        # Forgot password link
        st.markdown('<div style="text-align: right; margin: -5px 0 10px;"><a href="#" class="forgot-link">Forgot password?</a></div>', unsafe_allow_html=True)
        
        # Login button
        login_button = st.button("LOGIN")
        
        if login_button:
            with st.spinner('Authenticating...'):
                time.sleep(1)
                if username == "admin" and password == "admin123":
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid credentials")
        
        # Social login options
        st.markdown('<div style="text-align: center; margin: 20px 0 15px; color: #666; font-size: 13px;">Or Sign In With</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="social-icons">
                <a href="https://facebook.com" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/124/124010.png" class="social-icon" alt="Facebook">
                </a>
                <a href="https://twitter.com" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/124/124021.png" class="social-icon" alt="Twitter">
                </a>
                <a href="https://google.com" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/300/300221.png" class="social-icon" alt="Google">
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        # Sign up link
        st.markdown("""
            <div class="auth-links">
                Don't have an account? <a href="#">Sign Up</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_form()
else:
    st.write("Welcome to the application!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()