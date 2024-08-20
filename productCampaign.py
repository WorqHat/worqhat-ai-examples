import requests
import time
import streamlit as st
import json
import base64

def callapi(fileArray, api_key):
    start_time = time.time()  
    url = "https://api.worqhat.com/api/ai/content/v4"  
    payload = {
        "question": "I am sending you some images which denote a product that I have come up with. I want you to look at the images and first return the objects and features you can see,Then a Heading which will be the name of the product  and then a subheading which will be a tagline of the product and then a marketing campaign for the said product  in a JSON format", 
        "training_data": "You have to look at the images and get the objects and features in a json file and also write a marketing campaign make it attractive with headings and hashtags maybe use cases about the product in the images,Return the json with keys objects_and_features,Heading,Subheading,Marketing Campaign ",
        "response_type":"json",
        "model": "aicon-v4-nano-160824",
    }
    
    headers = {
        
        "Authorization": f"Bearer {api_key}",
      
    }

    st.write("The request is being sent")
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=fileArray)
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
        (
            'files', 
            (image.name, image.read(), image.type)
        )
        for image in uploaded_images
    ]
    response_v2, duration_v2 = callapi(files, api_key)

    if response_v2:
        content = response_v2.get('content', '')

        # Debug: Print the entire content to understand its structure
        st.write("Response Content:")
        st.json(content)  # This will print the entire JSON content in a formatted way

        # Parse the content string into a dictionary
        try:
            parsed_content = json.loads(content)
            st.success(f"Product campaign created successfully - Time taken: {duration_v2} seconds")
            
            # Print each part on a separate line
            st.markdown(f"**Objects and Features:** {', '.join(parsed_content.get('objects_and_features', []))}")
            st.markdown(f"**Heading:** {parsed_content.get('Heading', '')}")
            st.markdown(f"**Subheading:** {parsed_content.get('Subheading', '')}")
            st.markdown(f"**Marketing Campaign:**", unsafe_allow_html=True)
            st.markdown(parsed_content.get('Marketing Campaign', ''), unsafe_allow_html=True)
        except json.JSONDecodeError:
            st.write("Failed to parse the response content. Please check the API response.")
        
    else:
        st.write("Failed to create the product campaign.")

st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105).")
