# 🎙️ Speechii – AI-Powered Text-to-Speech & YouTube Summarizer

Speechii is a Streamlit-based application that converts text into speech, summarizes YouTube videos using AI, and stores user activity with a simple yet powerful backend.  
It includes user authentication, history tracking, an admin dashboard, and Redis-based caching to improve performance.

---

## 🚀 Features

### 🔊 1. Text-to-Speech Converter
- Convert any text into high-quality speech using **gTTS**.
- Supports multiple languages.
- Choose between **Normal** and **Slow** speed.
- Audio preview available after conversion.
- Each conversion is automatically saved to the user’s history.


### Technical workflow

<p align="center">
  <img src="assets/TTS Workflow.png" width="80%">
</p>

---

### 📜 2. User History
- Displays all past conversions with:
  - Timestamp  
  - Language & speed  
  - Text preview  
  - Playable audio
- Users can delete individual entries.
- Data stored in a persistent database.

---

### 🎥 3. YouTube Video Summarizer (with Redis Cache)

Speechii provides a smart summarization system for YouTube videos.

#### 🔄 How it Works
1. **Check Redis Cache**
   - When a YouTube link is entered, Speechii checks Redis Cloud.
   - If a stored summary exists → instantly returned.

2. **If not cached → Fetch transcript**
   - Use **YouTube Transcript API**  
   - If transcript is unavailable → fallback to **YouTube Data API**

3. **Summarize using Gemini API**
   - High-quality summarization done using **Google Gemini (Generative AI)**.

4. **Store Result in Redis**
   - Saved in Redis for instant future retrieval.

### Technical workflow

<p align="center">
  <img src="assets/YT Workflow.png" width="80%">
</p>


#### ⚡ Benefits
- Ultra-fast repeated queries  
- Reduced API cost  
- Avoids fetching transcript repeatedly  
- Less load on YouTube & Gemini API  

---

## 🙍‍♂️ Profile Page
Shows key user details:
- Username  
- Email  
- Role (user/admin)  

Also includes a **Logout** option to clear session.

---

## 🛠️ Admin Panel
Admins have additional privileges:

### Admin Can:
- View all registered users  
- View all user history entries  
- Monitor usage  
- Manage content  

This ensures better control over the platform.

---

## 🧰 Tech Stack

### Frontend
- **Streamlit**

### Backend
- **Python**
- **gTTS** → Text-to-Speech engine  
- **Redis Cloud** → Caching for YouTube Summaries  
- **SQLite / MySQL** → User & History storage  

### AI & APIs
- **YouTube Transcript API**  
- **YouTube Data API** (fallback)  
- **Google Gemini API** (summarization engine)

### Authentication
- **Streamlit Session State**  
- Custom login & role-based access  

### Storage
- History saved with:  
  - Text, language, speed, audio file, timestamp  
- Audio files stored locally with `tempfile`

---


## 📂 Project Structure

│── main.py # App entry point & routing
│── app.py # Text-to-Speech module
│── yt_summary.py # YouTube summarization workflow
│── login.py # Authentication system
│── utils.py # Database + helper functions
│── requirements.txt
│── README.md