import streamlit as st
import requests
import json

WORQHAT_ENDPOINT_URL = "https://api.worqhat.com/api/ai/content/v4"

st.title("Complaint Analysis")

# Function to process the complaint
def process_complaint(api_key, audio_file, order_notes, damaged_image, correct_image):
    url = WORQHAT_ENDPOINT_URL
    headers = {'Authorization': f'Bearer {api_key}'}

    files = [
        ('files', (audio_file.name, audio_file, audio_file.type)),
        ('files', (damaged_image.name, damaged_image, damaged_image.type)),
        ('files', (correct_image.name, correct_image, correct_image.type))
    ]

    data = {
        'model': 'aicon-v4-nano-160824',
        "question": "analyze the complaint. use the audio file to analyse the conversation and the images to analyse the damage. also use the order notes to understand the context. return the output in the json format\n\n  Order Notes: " + order_notes,
        "response_type": "json",
        "training_data": """damage analysis is the comparison between the two images. the output should be a score between 0 and 10. return the output in the following json format:
                                    {
                                    "damage analysis": {
                        "type": "score",
                        "range": [0, 10],
                        "description": "Damage score indicating the level of damage from 0 (no damage) to 10 (severely damaged). the first image is the damaged product and the second image is the correct product"
                    },
                                            "audio analysis": {
                            "emotions": "Summary of detected emotions of the customer in the audio file.",
                            "summary": "Brief summary of the complaint.",
                            "potential_resolution": "Potential resolution for the complaint as addressed by the customer.",
                            "key_points": "List of notable points mentioned in the complaint."
                        },
                        summary: summary of everything combined including the order notes

        }
"""
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        print("Response received:", json.dumps(result, indent=4))
        st.success("Complaint processed successfully!")
        st.json(result)
    else:
        print("Error:", response.status_code, response.text)
        st.error(f"Error processing complaint: {response.text}")

# API Key input
api_key = st.text_input("Enter WORQHAT API Key", type="password")

# Audio conversation input
audio_file = st.file_uploader("Upload Audio Conversation", type=["wav", "mp3"])

# Additional order notes input
order_notes = st.text_area("Additional Order Notes")

# Image inputs
damaged_image = st.file_uploader("Upload Damaged Product Image", type=["jpg", "jpeg", "png"])
correct_image = st.file_uploader("Upload Correct Product Image", type=["jpg", "jpeg", "png"])

# Analyze complaint button
if st.button("Analyze Complaint"):
    if api_key and audio_file and damaged_image and correct_image:
        process_complaint(api_key, audio_file, order_notes, damaged_image, correct_image)
    else:
        st.warning("Please upload all required files and enter the API key.")
