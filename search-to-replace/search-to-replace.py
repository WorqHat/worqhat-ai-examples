import requests
import time
import streamlit as st

def callapi(file,search,mod, api_key):
    start_time = time.time()  # Record start time
    url = "https://api.worqhat.com/api/ai/images/modify/v3/search-replace-image"
    payload = {
        "search_object" : [search],
        "modification": [mod] ,
        "output_type": "url"
    }
    files = {
        'existing_image': file  # Pass the file directly
    }
    headers = {

        'Accept': 'application/json',
        "Authorization": f"Bearer {api_key}"
    }
    st.write("The request is being sent")
    response = requests.request("POST",url, headers=headers, data=payload, files=files)
    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    if response.status_code == 200:
        return response.json()['image'], round(duration, 2)
    else:
        st.write("The request failed")
        return None, round(duration, 2)

st.title("Search and Replace Objects in Image")
st.write("Leverage the power of AI to dynamically search and replace objects within images. Ideal for e-commerce, marketing, and personalization, this API transforms your images with precision and creativity in just one step.")

st.markdown(
    "To use this API, you need an API key. If you don't have one, please sign up at [WorqHat API Signup Page](https://app.worqhat.com).")


uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
api_key = st.text_input("Enter WorqHat API Key:", type="password")
prompt1 = st.text_input("Enter The object to search")
prompt2 = st.text_input("Enter the modification you want to do ")
if st.button("Send"):
    st.write("Generating the image ")
    response_v2, duration_v2 = callapi(uploaded_image,prompt1, prompt2, api_key)
    st.image(response_v2, caption=f"Modified image - Time taken: {duration_v2} seconds", use_column_width=True)

st.write("Leverage the power of AI to dynamically search and replace objects within images. Ideal for e-commerce, marketing, and personalization, this API transforms your images with precision and creativity in just one step.")
st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com/ai-models/image-generation/search-to-replace) and the [API Reference page](https://docs.worqhat.com/api-reference/ai-models/image-generation/search-to-replace).")