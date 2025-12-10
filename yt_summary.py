import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai
import os
import dotenv
from redis_client import r   # your redis connection file

dotenv.load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_video_id(link_or_id: str) -> str:
    if "youtube.com" in link_or_id or "youtu.be" in link_or_id:
        if "v=" in link_or_id:
            return link_or_id.split("v=")[1].split("&")[0]
        if "youtu.be/" in link_or_id:
            return link_or_id.split("youtu.be/")[1].split("?")[0]
    return link_or_id


def get_transcript_youtube(video_id):
    """Try official YouTube transcript API."""
    try:
        formatter = TextFormatter()
        raw = YouTubeTranscriptApi.get_transcript(video_id)
        return formatter.format_transcript(raw)
    except:
        return None


def get_transcript_gemini(video_url):
    """Fallback transcript extraction using Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
    YouTube transcript is not available through API.
    Extract a clean FULL transcript of the video.

    Video: {video_url}

    Return ONLY the transcript (no summary).
    """

    resp = model.generate_content(prompt)
    return resp.text.strip()


def summarize(text):
    """Generate summary using Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
    Summarize this YouTube transcript clearly and in simple words:

    {text}
    """

    resp = model.generate_content(prompt)
    return resp.text


def show_yt_summary():
    st.title("YouTube → AI Summary")
    youtube_link = st.text_input("Enter YouTube URL")

    if st.button("Generate Summary"):

        if not youtube_link.strip():
            st.error("Enter a valid YouTube link!")
            return

        video_id = extract_video_id(youtube_link)

        # 1️⃣ FIRST: CHECK REDIS SUMMARY

        cached_summary = r.get(f"summary:{video_id}")

        if cached_summary:
            st.success("⚡ Loaded from Redis Summary Cache!")
            st.write(cached_summary)   # <-- FIXED
            return


        # 2️⃣ NOT IN REDIS → Try YouTube Transcript API
        with st.spinner("📥 Fetching transcript from YouTube..."):
            transcript = get_transcript_youtube(video_id)

        if transcript is None:
            st.warning("❌ YouTube transcript not available. Trying Gemini transcript...")

            # 3️⃣ FALLBACK → Use Gemini to extract transcript
            with st.spinner("🤖 Extracting transcript using Gemini..."):
                transcript = get_transcript_gemini(youtube_link)

        # Store transcript in Redis
        r.set(f"transcript:{video_id}", transcript)

        # 4️⃣ SUMMARIZE
        with st.spinner("🧠 Summarizing using Gemini..."):
            summary = summarize(transcript)

        # Save summary in Redis
        r.set(f"summary:{video_id}", summary)

        st.success("✔ Summary Generated!")
        st.write(summary)
