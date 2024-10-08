import requests
import time
import streamlit as st


def callapi(file, api_key, modification):
    start_time = time.time()  # Record start time
    url = "https://api.worqhat.com/api/ai/images/modify/v3/replace-background"
    payload = {"output_type": "url", "modification": modification}
    files = {'existing_image': file}
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {api_key}"  # Use the api_key variable
    }
    st.write("The request is being sent")
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    if response.status_code == 200:
        return response.json()['image'], round(duration, 2)
    else:
        st.write("The request failed")
        return None, round(duration, 2)


st.title("Replace Image Background using ImageCon API")
st.write("This API can replace the original background of images according to the user's requirements with just a single prompt, ensuring the main subject is highlighted effectively.")

st.markdown(
    "To use this API, you need an API key. If you don't have one, please sign up at [WorqHat API Signup Page](https://app.worqhat.com).")

uploaded_image = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_image is not None:
    # Check the size of the uploaded file
    file_size = uploaded_image.size
    # Convert bytes to megabytes
    file_size_mb = file_size / (1024 * 1024)

    # If the file size exceeds 16 MB, display a warning and set uploaded_image to None
    if file_size_mb > 16:
        st.warning(
            "The uploaded file exceeds the 16 MB size limit. Please upload a smaller file.")
        uploaded_image = None
    else:
        # Proceed with processing the uploaded image
        st.success("File uploaded successfully.")

api_key = st.text_input("Enter WorqHat API Key:", type="password")
modification = st.text_input("Enter the Modification for the Background")

if st.button("Send") and uploaded_image is not None:
    st.write("Generating the image ")
    response_v2, duration_v2 = callapi(uploaded_image, api_key, modification)

    col1, col2 = st.columns(2)  # Create two columns
    with col1:
        st.image(uploaded_image, caption="Input image")
    with col2:
        if response_v2:
            st.image(
                response_v2, caption=f"Modified image - Time taken: {duration_v2} seconds")
        else:
            st.write("Failed to generate the image.")

st.write("This API can replace the original background of images according to the user's requirements with just a single prompt, ensuring the main subject is highlighted effectively.")
st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com/ai-models/image-generation/replace-image-background) and the [API Reference page](https://docs.worqhat.com/api-reference/ai-models/image-generation/replace-image-background).")