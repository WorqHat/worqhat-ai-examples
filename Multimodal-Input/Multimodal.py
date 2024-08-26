import requests
import time
import streamlit as st
import json

def callapi(fileArray, api_key, text_input):
    start_time = time.time()
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": f"Please analyze the provided text, audio, video, and image files. Based on these inputs, generate a multimodal response that incorporates the key elements from each modality. Ensure the response is cohesive and utilizes the unique aspects of each input type. \n The text provided is {text_input}",
        "training_data": f"Analyze the provided text, audio, video, and image files. Create a cohesive response that incorporates the thought process from the text while considering the context provided by the audio, video, and image files. Return the result in markdown format with appropriate subheadings, and keep the key as multimodal_response.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    st.write("The request is being sent...")
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=fileArray)
    end_time = time.time()  
    duration = end_time - start_time  
    if response.status_code == 200:
        return response.json(), round(duration, 2)
    else:
        st.write("The request failed.")
        return None, round(duration, 2)

# Streamlit page setup
st.title("🖼️ Multimodal Content Generator 🌟")
st.write("""
Welcome to the **Multimodal Content Generator** tool! 🎉  
This tool helps you create a comprehensive response by combining text, audio, video, and image inputs.
Using the advanced **WorqHat API**, we ensure that all aspects of your inputs are considered in the generated content.
""")

st.markdown("**Steps to use this tool:**")
st.markdown("""
1. **Enter your API key:** If you don't have one, sign up at [WorqHat API Signup Page](https://app.worqhat.com).
2. **Provide your text input:** Enter the content you want to include.
3. **Upload audio files:** These should contain your thoughts or discussions.
4. **Upload video files:** These videos should be related to your thought process.
5. **Upload image files:** These images should be relevant to your content.
6. **Click 'Generate Content':** The tool will analyze your inputs and generate a cohesive multimodal response for you.
""")

st.markdown("**Let's get started!** 🚀")

text_input = st.text_area("✏️ Enter your text here:", height=150)

uploaded_audios = st.file_uploader(
    "🎧 Upload audio files...", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

uploaded_videos = st.file_uploader(
    "🎥 Upload video files...", type=["mp4", "avi", "mov"], accept_multiple_files=True)

uploaded_images = st.file_uploader(
    "🖼️ Upload image files...", type=["jpg", "jpeg", "png", "gif"], accept_multiple_files=True)

# Check if any files are uploaded
if uploaded_audios or uploaded_videos or uploaded_images:
    total_file_size_mb = sum(file.size for file in uploaded_audios + uploaded_videos + uploaded_images) / (1024 * 1024)
    
    if total_file_size_mb > 16:
        st.warning("🚨 The total size of the uploaded files exceeds the 16 MB limit. Please upload smaller files.")
        uploaded_audios, uploaded_videos, uploaded_images = [], [], []
    else:
        st.success("✅ Files uploaded successfully.")
else:
    total_file_size_mb = 0

api_key = st.text_input("🔑 Enter WorqHat API Key:", type="password")

if st.button("Generate Content") and text_input and (uploaded_audios or uploaded_videos or uploaded_images):
    st.write("✨ Generating your content... This may take a moment.")
    
    files = [
        ('files', (file.name, file.read(), file.type))
        for file in uploaded_audios + uploaded_videos + uploaded_images
    ]
    
    response_v2, duration_v2 = callapi(files, api_key, text_input)

    if response_v2:
        content = response_v2.get('content', '')
        try:
            parsed_content = json.loads(content)
            st.success(f"✅ Content generated successfully! (Time taken: {duration_v2} seconds)")
            st.markdown(parsed_content.get('multimodal_response', ''))
        except json.JSONDecodeError:
            st.error("❌ Failed to parse the response content. Please check the API response.")
    else:
        st.error("❌ Failed to generate the content.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
