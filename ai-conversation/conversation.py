import streamlit as st
import requests
import json
import uuid

# Generate a random UUID for the conversation ID
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# API Key input (hidden)
api_key = st.sidebar.text_input("Enter WORQHAT API Key", type="password")

if not api_key:
    st.warning("Please enter the WORQHAT API Key to proceed.")
else:
    # Display the conversation ID
    st.write(f"Conversation ID: {st.session_state.conversation_id}")

    def send_files_and_question(files, question, training_data, first_message):
        url = 'https://api.worqhat.com/api/ai/content/v4'
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {
            'question': question,
            'training_data': training_data,
            'model': 'aicon-v4-nano-160824',
            'conversation_id': st.session_state.conversation_id
        }
        # Conditionally include files only if it's the first message
        if first_message:
            files_to_send = [('files', (file.name, file, file.type)) for file in files]
            response = requests.post(url, headers=headers, files=files_to_send, data=data)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get('content', '')
            if content:
                st.session_state.chat_history.append({'sender': 'Bot', 'message': content})
        else:
            st.error(f"Error: {response.status_code}, {response.text}")

    # Initialize session state to store chat history and first message flag
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'first_message_sent' not in st.session_state:
        st.session_state.first_message_sent = False

    # File uploader
    uploaded_files = st.sidebar.file_uploader("Upload your files", type=["pdf", "png", "jpg"], accept_multiple_files=True)

    # Chat interface
    user_input = st.chat_input("Ask a question:", key="chat_input")
    if user_input:
        # Append user question to chat history
        st.session_state.chat_history.append({'sender': 'User', 'message': user_input})

        # Process the question if files are uploaded
        if uploaded_files and not st.session_state.first_message_sent:
            send_files_and_question(uploaded_files, user_input, "You are Alex and you are one of the best Financial Analyst who is trained to understand and answer all kinds of financial data.", True)
            st.session_state.first_message_sent = True  # Set the flag after sending the first message
        elif user_input:
            send_files_and_question([], user_input, "You are Alex and you are one of the best Financial Analyst who is trained to understand and answer all kinds of financial data.", False)

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat['sender']):
            st.write(chat['message'])
