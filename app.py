import streamlit as st
from gtts import gTTS
import tempfile
from utils import (
    save_history,
    LANGUAGE_MAP,
    get_user_history,
    get_all_users,
    get_all_history,
    delete_history_entry
)

def show_app():
    st.title("🎙️ Speechii")

    tabs = ["🔊 Convert", "📜 My History", "🙍‍♂️ Profile"]
    if st.session_state.role == "admin":
        tabs.append("🛠️ Admin Panel")

    tab1, tab2, tab3, *optional_tabs = st.tabs(tabs)

    # 🔊 Convert Tab
    with tab1:
        st.subheader("Convert Text to Speech")
        text = st.text_area("Enter text")

        language_full = st.selectbox("Language", list(LANGUAGE_MAP.values()))
        language = [k for k, v in LANGUAGE_MAP.items() if v == language_full][0]

        speed = st.radio("Speed", ["Normal", "Slow"])

        if st.button("Convert"):
            if text.strip():
                tts = gTTS(text=text, lang=language, slow=(speed == "Slow"))
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    save_history(st.session_state.username, text, language, speed, fp.name)
                    st.audio(fp.name)
                    st.success("Conversion completed.")
            else:
                st.warning("Please enter some text.")

    # 📜 History Tab
    with tab2:
        st.subheader("📜 Your Conversion History")
        rows = get_user_history(st.session_state.username)
        if rows:
            for entry in rows:
                entry_id, text, lang, speed, file, timestamp = entry if len(entry) == 6 else (None, *entry)
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.markdown(f"🕒 `{timestamp}` — **{LANGUAGE_MAP.get(lang, lang)} / {speed}**")
                    st.text(text[:100] + "...")
                    st.audio(file)
                with col2:
                    if st.button("🗑️", key=f"del_{entry_id}"):
                        delete_history_entry(entry_id, st.session_state.username)
                        st.success("Deleted.")
                        st.rerun()
        else:
            st.info("No history found.")

    # 🙍‍♂️ Profile Tab
    with tab3:
        st.subheader("🙍‍♂️ Your Profile")
        st.markdown(f"**Username:** `{st.session_state.username}`")
        st.markdown(f"**Email:** `{st.session_state.email}`")
        st.markdown(f"**Role:** `{st.session_state.role}`")
        st.markdown("---")
        if st.button("🔓 Logout", key="logout_btn_profile"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    # 🛠️ Admin Panel
    if st.session_state.role == "admin" and optional_tabs:
        with optional_tabs[0]:
            st.subheader("🛠️ Admin Dashboard")
            st.write("👤 Registered Users:")
            for email, uname, role in get_all_users():
                st.markdown(f"**{uname}** - {email} - `{role}`")
            st.write("---")
            st.write("📜 All Conversion History:")
            for uname, text, lang, speed, ts in get_all_history():
                lang_name = LANGUAGE_MAP.get(lang, lang)
                st.markdown(f"**{uname}** — *{ts}* — `{lang_name}` / `{speed}`")
                st.text(text[:100] + "...")
