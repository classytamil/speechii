import streamlit as st
from utils import add_user, verify_user

def show_login():
    st.title("🔐 Speechii Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # 🔐 Login Tab
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            valid, uname, role = verify_user(email, password)
            if valid:
                st.session_state.authenticated = True
                st.session_state.username = uname
                st.session_state.email = email  # ✅ Add this line
                st.session_state.role = role
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Invalid credentials.")

    # 📝 Register Tab
    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email (Register)")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")

        if submitted:
            if password != confirm:
                st.error("Passwords do not match.")
            elif email and username:
                try:
                    add_user(email, username, password)
                    st.success("Registered! You can now login.")
                except:
                    st.error("User already exists.")
