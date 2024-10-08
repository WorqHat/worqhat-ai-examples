import requests
import time
import streamlit as st
import json

def callapi(from_name, to_name, email_topic, api_key):
    start_time = time.time()
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": f"Please draft an email from {from_name} to {to_name} about {email_topic}.",
        "training_data": "The response should include both an 'email_subject' and 'email_body'. The subject should be concise and to the point in a proper sentence dont just use words. The email body should be written in a professional tone, with proper salutation, a clear introduction, body content, and a closing statement. The final response should be a JSON object with 'email_subject' and 'email_body' as separate fields.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    st.write("The request is being sent...")
    response = requests.post(url, headers=headers, json=payload)
    end_time = time.time()  
    duration = end_time - start_time  
    if response.status_code == 200:
        return response.json(), round(duration, 2)
    else:
        st.write("The request failed.")
        return None, round(duration, 2)

# Streamlit page setup
st.title("📧 Email Generator 📧")
st.write("""
Welcome to the **Email Generator** tool! 🚀  
This tool helps you generate professional emails quickly by using the **WorqHat API**.
""")

st.markdown("**Steps to use this tool:**")
st.markdown("""
1. **Enter your API key:** If you don't have one, sign up at [WorqHat API Signup Page](https://app.worqhat.com).
2. **Enter 'From' and 'To' names:** These should be the full names of the sender and the recipient.
3. **Provide the email topic:** A brief description of what the email is about.
4. **Click 'Generate Email':** The tool will generate a professional email based on the information you provide.
""")

# Input fields for the email details
from_name = st.text_input("👤 From Name:")
to_name = st.text_input("👤 To Name:")
email_topic = st.text_input("📝 What is the email about? (Email Topic)")

# API key input
api_key = st.text_input("🔑 Enter WorqHat API Key:", type="password")

# Generate email button
if st.button("Generate Email") and from_name and to_name and email_topic:
    st.write("✨ Generating your Email... This may take a moment.")
    
    # Call the API with the input details
    response_v2, duration_v2 = callapi(from_name, to_name, email_topic, api_key)

    if response_v2:
        content = response_v2.get('content', '')
        
        try:
            parsed_content = json.loads(content)
            
            st.success(f"✅ Email generated successfully! (Time taken: {duration_v2} seconds)")
            
            # Display the generated email subject and body separately
            st.markdown(f"### ✉️ Subject: \n**{parsed_content.get('email_subject', 'No subject generated')}**")
            st.markdown(f"### 📝 Content: \n{parsed_content.get('email_body', 'No email content generated')}")
        except json.JSONDecodeError:
            st.error("❌ Failed to parse the response content. Please check the API response.")
    else:
        st.error("❌ Failed to generate the email.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
