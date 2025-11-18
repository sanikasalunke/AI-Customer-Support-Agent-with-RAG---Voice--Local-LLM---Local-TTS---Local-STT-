# ui/app.py
import streamlit as st
import requests
import os
from api.main import app  # optional local import; or call endpoints via requests
API_BASE = "http://localhost:8000"

st.title("AI Customer Support — Demo")

if "session_id" not in st.session_state:
    r = requests.post(f"{API_BASE}/session/start")
    st.session_state.session_id = r.json()["session_id"]

sid = st.session_state.session_id

st.header("Text chat")
user = st.text_input("Your message")
if st.button("Send text"):
    r = requests.post(f"{API_BASE}/session/{sid}/message", json={"text": user})
    st.text_area("Assistant", value=r.json()["reply"], height=200)

st.header("Voice chat (upload)")
audio_file = st.file_uploader("Upload audio (wav/m4a)", type=["wav","m4a","mp3"])
if audio_file is not None:
    files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
    r = requests.post(f"{API_BASE}/session/{sid}/audio", files=files)
    st.write("Transcript:", r.json()["transcript"])
    st.write("Reply:", r.json()["reply"])
    wav_path = r.json().get("wav")
    if wav_path and os.path.exists(wav_path):
        st.audio(wav_path)
