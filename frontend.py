import streamlit as st
import requests  # To call your FastAPI endpoint

# --------------------------------------------------------
# Streamlit page title
st.title("FastAPI + Streamlit Chatbot")

# --------------------------------------------------------
# This keeps your conversation memory in the browser session
# The session_state dict is stored on the user's side and persists until refresh
if "messages" not in st.session_state:
    # Initialize the chat history with an empty list
    st.session_state.messages = []

# --------------------------------------------------------
# Show the conversation so far
# Loop through each message and display it
for msg in st.session_state.messages:
    # Display user messages on left
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    # Display assistant messages on right
    else:
        st.chat_message("assistant").write(msg["content"])

# --------------------------------------------------------
# This is the text input box at the bottom
# It returns the text once you hit Enter
user_input = st.chat_input("Type your message here...")

# --------------------------------------------------------
# If the user typed something:
if user_input:
    # Add the user's message to the local session_state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # --------------------------------------------------------
    # Call your FastAPI backend with POST request
    # Replace with your actual FastAPI URL
    response = requests.post(
        "http://127.0.0.1:8002/chat",
        json={"message": user_input}
    )

    # The FastAPI returns just the text, so get it:
    bot_reply = response.text

    # Add the assistant's reply to the local session_state
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Rerun the Streamlit app to show the new message immediately
    st.rerun()
