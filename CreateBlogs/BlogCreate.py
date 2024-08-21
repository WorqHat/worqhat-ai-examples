import requests
import time
import streamlit as st
import json

def callapi(fileArray, api_key):
    start_time = time.time()
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": "I am sending you some audio files that discuss my thought process. I also have provided two blog entries. Draft my next blog post based on my thoughts in this audio file and these two previous blog posts I wrote. Please return the Blog in a formatted way to be directly uploaded on blog sites",
        "training_data": "Analyze the audio and blog content provided, identify key insights, summarize the thought process and notice the writing style. Create a blog expanding on the thought process and keep the writing style similar to the blogs. Return the JSON with keys: insights, summary, unified_theme.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    st.write("The request is being sent")
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=fileArray)
    end_time = time.time()  
    duration = end_time - start_time  
    if response.status_code == 200:
        return response.json(), round(duration, 2)
    else:
        st.write("The request failed")
        return None, round(duration, 2)

st.title("Blog Generator ")
st.write("This tool allows you to upload blogs and audio files discussing your thought process, and it will generate a blog for you keeping your thought process and writing style in mind using the WorqHat API.")

st.markdown("To use this tool, please enter your API key. If you don't have one, sign up at [WorqHat API Signup Page](https://app.worqhat.com).")

blog1 = st.text_area("Enter your first blog here:")
blog2 = st.text_area("Enter your second blog here:")

uploaded_audios = st.file_uploader(
    "Upload audio files discussing your thought process...", type=["mp3", "wav"], accept_multiple_files=True)

if uploaded_audios:
    total_file_size = sum(audio.size for audio in uploaded_audios)
    total_file_size_mb = total_file_size / (1024 * 1024)

    if total_file_size_mb > 16:
        st.warning(
            "The total size of the uploaded files exceeds the 16 MB size limit. Please upload smaller files.")
        uploaded_audios = []
    else:
        st.success("Audio files uploaded successfully.")

api_key = st.text_input("Enter WorqHat API Key:", type="password")

if st.button("Send") and blog1 and blog2 and uploaded_audios:
    st.write("Generating the your Blog...")
    files = [
        ('files', (audio.name, audio.read(), audio.type))
        for audio in uploaded_audios
    ]
    response_v2, duration_v2 = callapi(files, api_key)

    if response_v2:
        content = response_v2.get('content', '')

        try:
            parsed_content = json.loads(content)
            st.success(f"Analysis generated successfully - Time taken: {duration_v2} seconds")
            
            st.markdown(f"**Insights:** {', '.join(parsed_content.get('insights', []))}")
            st.markdown(f"**Summary:** {parsed_content.get('summary', '')}")
            st.markdown(f"**Unified Theme:** {parsed_content.get('unified_theme', '')}")
        except json.JSONDecodeError:
            st.write("Failed to parse the response content. Please check the API response.")
        
    else:
        st.write("Failed to generate the analysis.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")