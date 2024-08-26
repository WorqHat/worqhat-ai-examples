import streamlit as st
import requests
import time
import json

# Set page configuration
st.set_page_config(page_title="Multimodal Chat App", page_icon="🗨️", layout="centered")

# Function to call the API
def call_api(file_data, text_input, api_key):
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": f"Please analyze the provided text, audio, video, and image files. Respond to this: {text_input}",
        "model": "aicon-v4-nano-160824",
        "training_data": "Respond in a friendly way, in content make the key to your answer as 'answer'",
        "response_type": "json",
        "conversation_id":123
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    try:
        response = requests.post(url, headers=headers, data=payload, files=file_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API key input
with st.sidebar:
    st.title("🔑 API Configuration")
    api_key = st.text_input("Enter your API key:", type="password")

st.title("🗨️ Multimodal Chat App")
st.write("Chat with the AI using text and various file types (audio, video, images).")

# Chat input area
if api_key:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["file"]:
                st.caption(f"Uploaded file: {message['file']['name']}")
                if message["file"]["type"].startswith("image/"):
                    st.image(message["file"]["data"])
                else:
                    st.write(f"File type '{message['file']['type']}' is not previewable.")
    
    # User input and file uploader
    prompt = st.text_input("Your message:", key="user_input")
    uploaded_file = st.file_uploader("Attach a file (optional):", type=["mp3", "wav", "ogg", "mp4", "avi", "mov", "jpg", "jpeg", "png", "gif"], key="file_uploader")
    
    # Button to send message
    if st.button("Send") and prompt:
        # Prepare file data
        file_data = None
        file_info = None
        if uploaded_file:
            file_bytes = uploaded_file.read()
            file_data = {
                'files': (uploaded_file.name, file_bytes, uploaded_file.type)
            }
            file_info = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "data": file_bytes
            }
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "file": file_info})
        
        # Call API and add AI response to chat history
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = call_api(file_data, prompt, api_key)
                if response and 'content' in response:
                    try:
                        content_dict = json.loads(response['content'])
                        ai_content = content_dict.get('answer', 'No response available.')
                    except json.JSONDecodeError:
                        ai_content = "❌ Failed to parse the response content."
                else:
                    ai_content = "❌ Failed to generate the content."
                
                st.markdown(ai_content)
                st.session_state.messages.append({"role": "assistant", "content": ai_content, "file": None})
        
        # Clear input field after sending
        st.experimental_rerun()
else:
    st.warning("Please enter your API key in the sidebar to start chatting.")

# Footer
st.markdown("---")
st.markdown("For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
