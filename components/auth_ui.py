import streamlit as st
from auth.auth_handler import AuthHandler

def initialize_session_state():
    """Initialize session state variables for authentication"""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def login_ui():
    """Display login form"""
    st.subheader("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")
        
        if submit:
            auth_handler = AuthHandler()
            success, result = auth_handler.authenticate_user(email, password)
            
            if success:
                st.session_state.user = result
                st.session_state.authenticated = True
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error(result)

def register_ui():
    """Display registration form"""
    st.subheader("Register")
    
    with st.form("register_form"):
        email = st.text_input("Email", key="register_email")
        name = st.text_input("Name", key="register_name")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        language = st.selectbox("Preferred Language", ["English", "Spanish", "French", "Chinese", "Arabic"], key="preferred_language")
        
        language_code = {"English": "en", "Spanish": "es", "French": "fr", "Chinese": "zh", "Arabic": "ar"}
        
        submit = st.form_submit_button("Register")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return
            
            auth_handler = AuthHandler()
            success, message = auth_handler.register_user(
                email=email,
                password=password,
                name=name,
                preferred_language=language_code.get(language, "en")
            )
            
            if success:
                st.success(message)
                st.info("You can now log in with your credentials")
            else:
                st.error(message)

def logout():
    """Handle user logout"""
    st.session_state.user = None
    st.session_state.authenticated = False
    st.experimental_rerun()

def auth_page():
    """Main authentication page that shows either login/register or user profile"""
    initialize_session_state()
    
    if st.session_state.authenticated:
        st.write(f"Welcome, {st.session_state.user.name or st.session_state.user.email}!")
        
        if st.button("Logout"):
            logout()
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_ui()
        
        with tab2:
            register_ui()
