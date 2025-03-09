import streamlit as st
from components.auth_ui import auth_page, initialize_session_state
from components.visualizer import twod_visualizer


st.set_page_config(
    page_title="Health Lens",
    page_icon="💊",
    layout="wide"
)

initialize_session_state()

st.sidebar.title("Language Simplifier")

# if not st.session_state.authenticated:
#     auth_page()
# else:
app_mode = st.sidebar.selectbox(
    "Select Feature",
    ["Prescription Scanner", "Drug Effect Visualizer",  "Medical Term Translator", "Health Dashboard"]
)

# st.sidebar.write(f"Logged in as: {st.session_state.user.email}")
# if st.sidebar.button("Logout"):
#     # st.session_state.user = None
#     # st.session_state.authenticated = False
#     st.rerun()

if app_mode == "Prescription Scanner":
    st.title("Prescription Scanner")
    st.write("This feature will be implemented next...")

elif app_mode == "Drug Effect Visualizer":
    st.title("Drug Effect Visualizer")
    twod_visualizer()
    # st.write("This feature will be implemented next...")

elif app_mode == "Medical Term Translator":
    st.title("Medical Term Translator")
    # st.write("This feature will be implemented next...")
    twod_visualizer()

elif app_mode == "Health Dashboard":
    st.title("Health Dashboard")
    st.write("This feature will be implemented next...")
