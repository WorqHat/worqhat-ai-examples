import streamlit as st
import requests
import json  # Import the json library
import random
# Function to call the API and generate story parts
def generate_story(api_key, prompt):
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": prompt,
        "training_data": "Provide a single, engaging continuation for the story.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_data = response.json()

        # Debug: Print the entire response to check the format
        st.write("API Response:", response_data)

        # Safely get the content and options
        content = response_data['content']
        # Parse the content string as JSON
        content_json = json.loads(content)
        story_part = content_json['story']
        return story_part

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.write("Response content:", response.text)
    return None

# Initialize session state variables
if 'current_story' not in st.session_state:
    st.session_state.current_story = ""
if 'story_stage' not in st.session_state:
    st.session_state.story_stage = "premise"

# Streamlit page setup
st.title("📝 Interactive Story Generator")

st.markdown("""
Welcome to the **Interactive Story Generator**!  
Create a unique story by iteratively selecting the direction of the narrative. 
Start with a premise, then choose how the story progresses at each step.
""")

# Step 1: Collect API key at the beginning
api_key = st.text_input("🔑 Enter WorqHat API Key:", type="password")

# Step 2: Generate and select the premise
if st.session_state.story_stage == "premise" and api_key:
    st.header("Step 1: Select or Generate a Premise")
    user_premise = st.text_input("Enter your story premise (or leave blank for a surprise):")

    if st.button("Surprise Me!"):
        random_prompts = [
            "A young detective stumbles upon a hidden world of magic.",
            "In a dystopian future, a rebel group plans a major heist.",
            "A stranded astronaut discovers an alien civilization on a distant planet."
        ]
        user_premise = random.choice(random_prompts)
        st.write(f"Surprise Premise: {user_premise}")

    if user_premise:
        st.session_state.current_story = user_premise
        st.session_state.story_stage = "beginning"

# Step 3: Generate and display the beginning
if st.session_state.story_stage == "beginning" and api_key:
    st.header("Step 2: The Beginning")

    if st.button("Generate Beginning"):
        prompt = f"Create the beginning of a story based on this premise: {st.session_state.current_story}"
        beginning = generate_story(api_key, prompt)

        if beginning:
            st.write(f"Beginning: {beginning}")
            st.session_state.current_story += " " + beginning
            st.session_state.story_stage = "middle"

# Step 4: Generate and display the middle part
if st.session_state.story_stage == "middle" and api_key:
    st.header("Step 3: The Middle")

    if st.button("Generate Middle"):
        prompt = f"Continue the story: {st.session_state.current_story}"
        middle = generate_story(api_key, prompt)

        if middle:
            st.write(f"Middle: {middle}")
            st.session_state.current_story += " " + middle
            st.session_state.story_stage = "climax"

# Step 5: Generate and display the climax part
if st.session_state.story_stage == "climax" and api_key:
    st.header("Step 4: The Climax")

    if st.button("Generate Climax"):
        prompt = f"Continue the story towards the climax: {st.session_state.current_story}"
        climax = generate_story(api_key, prompt)

        if climax:
            st.write(f"Climax: {climax}")
            st.session_state.current_story += " " + climax
            st.session_state.story_stage = "end"

# Step 6: Generate and display the ending
if st.session_state.story_stage == "end" and api_key:
    st.header("Step 5: The Ending")

    if st.button("Generate Ending"):
        prompt = f"Complete the story: {st.session_state.current_story}"
        ending = generate_story(api_key, prompt)

        if ending:
            st.write(f"Ending: {ending}")
            st.session_state.current_story += " " + ending
            st.success("🎉 Your story is complete!")
            st.markdown(f"### Final Story:\n{st.session_state.current_story}")

# Footer
st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105)."
)
