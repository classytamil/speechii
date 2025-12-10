# main.py
import streamlit as st
from utils import init_db
from login import show_login
from app import show_app
from yt_summary import show_yt_summary

st.set_page_config(page_title="Speechii", layout="centered")
init_db()

# Initialize session variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# If not logged in → show login
if not st.session_state.authenticated:
    show_login()

# If logged in → show menu
else:
    st.sidebar.title("Navigation")
    st.sidebar.write("---")

    choice = st.sidebar.radio("Go to:", ["Speechii App", "YouTube Summary"])

    if choice == "Speechii App":
        show_app()

    elif choice == "YouTube Summary":
        show_yt_summary()
