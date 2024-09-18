import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="Multimodal Chat App", page_icon="🗨️", layout="centered")

# Function to call the API
def call_api(text_input, api_key, file_data=None, conversation_id=None):
    url = "https://api.worqhat.com/api/ai/content/v4"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    if file_data:  # If file is uploaded
        payload = {
            "question": f"Please analyze the provided text, audio, video, and image files. Respond to this: {text_input}",
            "model": "aicon-v4-nano-160824",
            "training_data": "Respond in a friendly way, in content make the key to your answer as 'answer'",
            "response_type": "json",
            "conversation_id": conversation_id
        }
        try:
            response = requests.post(url, headers=headers, data=payload, files=file_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return None
    else:  # If no file is uploaded
        payload = {
            "question": f"Please analyze the provided text. Respond to this: {text_input}",
            "model": "aicon-v4-nano-160824",
            "training_data": "Respond in a friendly way, in content make the key to your answer as 'answer'",
            "response_type": "json",
            "conversation_id": conversation_id
        }
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# Sidebar for API key and conversation ID input
with st.sidebar:
    st.title("🔑 API Configuration")
    api_key = st.text_input("Enter your API key:", type="password")
    conversation_id = st.text_input("Enter a unique conversation ID:")

    # Update session state for conversation ID
    if conversation_id:
        st.session_state.conversation_id = conversation_id

st.title("🗨️ Multimodal Chat App")
st.write("Chat with the AI using text and various file types (audio, video, images).")

# Function to handle message submission
def submit():
    st.session_state.prompt = st.session_state.user_input  # Store the current input
    st.session_state.user_input = ''  # Clear the input field

# Function to handle file upload and clearing
def handle_file_upload():
    st.session_state.uploaded_file = uploaded_file  # Store uploaded file
    st.session_state.uploaded_file_bytes = uploaded_file.read()  # Read the file data

# Chat input area
if api_key and st.session_state.conversation_id:
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
    st.text_input("Your message:", key="user_input", on_change=submit)
    uploaded_file = st.file_uploader("Attach a file (optional):", type=["mp3", "wav", "ogg", "mp4", "avi", "mov", "jpg", "jpeg", "png", "gif"])

    # Store the uploaded file in session state
    if uploaded_file is not None:
        handle_file_upload()

    # Button to send message
    if st.button("Send") and st.session_state.prompt:
        # Prepare file data
        file_data = None
        file_info = None
        if uploaded_file:
            file_data = {
                'files': (uploaded_file.name, st.session_state.uploaded_file_bytes, uploaded_file.type)
            }
            file_info = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "data": st.session_state.uploaded_file_bytes
            }

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": st.session_state.prompt, "file": file_info})

        # Call API and add AI response to chat history
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = call_api(st.session_state.prompt, api_key, file_data, st.session_state.conversation_id)
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

        # Clear the uploaded file after sending the message
        st.session_state.uploaded_file = None
        st.session_state.uploaded_file_bytes = None

        # Rerun the app to refresh the UI
        st.rerun()

else:
    st.warning("Please enter your API key and conversation ID in the sidebar to start chatting.")

# Footer
st.markdown("---")
st.markdown("For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
