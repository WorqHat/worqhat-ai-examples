import requests
import time
import streamlit as st
import json
import base64

def callapi(fileArray, api_key):
    start_time = time.time()  
    url = "https://api.worqhat.com/api/ai/content/v4"  
    payload = json.dumps({
        "question": "I am sending you some images which denote a product that I have come up with. I want you to look at the images and first return the objects and features you can see in a JSON format and then write a marketing campaign about the said product.", 
        "training_data": "You have to look at the images and get the objects and features in a json file and also write a marketing campaign about the product in the images",
        "response_type":"json",
        "model": "aicon-v4-large-160824",
        "files":fileArray
    })
    
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {api_key}",
        'Content-Type':'application/json'
    }

    st.write("The request is being sent")
    response = requests.request(
        "POST", url, headers=headers, data=payload)
    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    if response.status_code == 200:
        return response.json(), round(duration, 2)
    else:
        print(response.json())
        st.write("The request failed")
        return None, round(duration, 2)


st.title("Create a Product Campaign using WorqHat API")
st.write("This API enables the creation of a product campaign from multiple images in a single API call, helping you generate marketing content based on the products in the images.")

st.markdown(
    "To use this API, you need an API key. If you don't have one, please sign up at [WorqHat API Signup Page](https://app.worqhat.com).")

uploaded_images = st.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_images:
    total_file_size = sum(image.size for image in uploaded_images)
    total_file_size_mb = total_file_size / (1024 * 1024)

    if total_file_size_mb > 16:
        st.warning(
            "The total size of the uploaded files exceeds the 16 MB size limit. Please upload smaller files.")
        uploaded_images = []
    else:
        st.success("Files uploaded successfully.")

api_key = st.text_input("Enter WorqHat API Key:", type="password")

if st.button("Send") and uploaded_images:
    st.write("Generating the product campaign...")
    files = [
        {
            'fieldname': 'images',
            'originalname': image.name,
            'mimetype': image.type,
            'buffer': base64.b64encode(image.read()).decode('utf-8'),  # Convert buffer to base64 string
            'size': image.size
        }
        for image in uploaded_images
    ]
    response_v2, duration_v2 = callapi(files, api_key)

    if response_v2:
        st.success(
            f"Product campaign created successfully - Time taken: {duration_v2} seconds")
        st.markdown(f"[View Campaign]({response_v2})")
    else:
        st.write("Failed to create the product campaign.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
