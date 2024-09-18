import streamlit as st
import requests
import json

st.set_page_config(page_title="📝 QuickStartApp")
st.title('📝 QuickStartApp')

worqhat_api_key = st.sidebar.text_input('WorqHat API Key')

def generate_response(input_text):
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": input_text,
        "training_data": "Provide a concise and informative response to the question. put the key as answer",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    headers = {
        "Authorization": f"Bearer {worqhat_api_key}",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        #st.write("API Response:", response_data)  # Print the API response for debugging
        content = response_data['content']
        content_json = json.loads(content)
        response_text = content_json['answer']  # Replace '<correct_key>' with the actual key
        st.info(response_text)  # Display the response from WorqHat

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.write("Response content:", response.text)

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if not worqhat_api_key.startswith('sk-'):
        st.warning('Please enter your WorqHat API key!', icon='⚠')
    if submitted and worqhat_api_key.startswith('sk-'):
        generate_response(text)
