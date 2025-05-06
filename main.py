# main.py
import streamlit as st
from utils import init_db
from login import show_login
from app import show_app

st.set_page_config(page_title="Speechii", layout="centered")
init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.page = "login"
if st.session_state.authenticated:
    show_app()
else:
    show_login()
