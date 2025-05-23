import streamlit as st
import main  # Imports your updated main.py
import speech_recognition as sr

# Title
st.set_page_config(page_title="Jarvis Assistant", layout="centered")
st.title("🤖 Jarvis - Your Voice Assistant")

# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display previous chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle voice input
recognizer = sr.Recognizer()
def listen_voice():
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio).lower()
            return query
        except:
            st.error("Could not recognize voice.")
            return ""

# Input area
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Ask something...", key="text_input")
with col2:
    if st.button("🎤"):
        user_input = listen_voice()

# When user sends message
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = main.handle_command_streamlit(user_input)

    st.session_state.chat.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
