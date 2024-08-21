import requests
import time
import streamlit as st
import json

def callapi(fileArray, api_key, blog1, blog2):
    start_time = time.time()
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": f"I am providing you with two blog entries that I previously wrote and some audio files that discuss my current thought process. Based on the audio, please draft my next blog post of exact or above 500 words. Ensure that the new blog aligns with the writing style of my previous blogs while incorporating the ideas from the audio recordings.Add Subheadings and make it as attractive to the reader as possible .Here are the blogs:\n\nBlog 1: {blog1}\n\nBlog 2: {blog2}",
        "training_data": f"Analyze the provided audio files and blog content.Create a cohesive blog post that expands on the thought process from the audio while maintaining a similar writing style to the provided blogs. Return the result in markdown format with one heading and subheadings and keep the key as blog_post. ",
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
st.title("✨ Blog Post Generator ✨")
st.write("""
Welcome to the **Blog Post Generator** tool! 🎉  
This tool helps you create a well-crafted blog post by combining the insights from your audio recordings and previous blog entries.  
Using the advanced **WorqHat API**, we ensure that your thought process and unique writing style are preserved in the generated content.
""")

st.markdown("**Steps to use this tool:**")
st.markdown("""
1. **Enter your API key:** If you don't have one, sign up at [WorqHat API Signup Page](https://app.worqhat.com).
2. **Provide your previous blog entries:** Enter the content of two blog posts that you have written before.
3. **Upload audio files:** These should contain your thoughts or discussions that you want to incorporate into the new blog post.
4. **Click 'Generate Blog':** The tool will analyze your inputs and generate a new blog post for you.
""")

st.markdown("**Let's get started!** 🚀")

blog1 = st.text_area("✏️ Enter your first blog here:", height=200)
blog2 = st.text_area("✏️ Enter your second blog here:", height=200)

uploaded_audios = st.file_uploader(
    "🎧 Upload audio files discussing your thought process...", type=["mp3", "wav","ogg"], accept_multiple_files=True)

if uploaded_audios:
    total_file_size = sum(audio.size for audio in uploaded_audios)
    total_file_size_mb = total_file_size / (1024 * 1024)

    if total_file_size_mb > 16:
        st.warning(
            "🚨 The total size of the uploaded files exceeds the 16 MB limit. Please upload smaller files.")
        uploaded_audios = []
    else:
        st.success("✅ Audio files uploaded successfully.")

api_key = st.text_input("🔑 Enter WorqHat API Key:", type="password")

if st.button("Generate Blog") and blog1 and blog2 and uploaded_audios:
    st.write("✨ Generating your Blog... This may take a moment.")
    files = [
        ('files', (audio.name, audio.read(), audio.type))
        for audio in uploaded_audios
    ]
    response_v2, duration_v2 = callapi(files, api_key, blog1, blog2)

    if response_v2:
        print(response_v2)
        content = response_v2.get('content', '')

        try:
            parsed_content = json.loads(content)
            st.success(f"✅ Blog generated successfully! (Time taken: {duration_v2} seconds)")
            
            st.markdown(parsed_content.get('blog_post', ''))
        except json.JSONDecodeError:
            st.error("❌ Failed to parse the response content. Please check the API response.")
        
    else:
        st.error("❌ Failed to generate the blog post.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
