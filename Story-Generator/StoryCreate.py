import streamlit as st
import requests
import random
import json

# Function to call the API and generate story parts
def generate_story(api_key, prompt, stage):
    url = "https://api.worqhat.com/api/ai/story/v4"
    payload = {
        "question": prompt,
        "training_data": f"Create a {stage} part of the story. Provide three different options for the user to choose from.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.write("The request failed.")
        return None

# Streamlit page setup
st.title("📝 Interactive Story Generator")

st.markdown("""
Welcome to the **Interactive Story Generator**!  
Create a unique story by iteratively selecting the direction of the narrative. 
Start with a premise, then choose how the story progresses at each step.
""")

# Step 1: User provides or generates a premise
st.header("Step 1: Select or Generate a Premise")
user_premise = st.text_input("Enter your story premise (or leave blank for a surprise):")

if st.button("Surprise Me!"):
    # Generate a random premise
    random_prompts = [
        "A young detective stumbles upon a hidden world of magic.",
        "In a dystopian future, a rebel group plans a major heist.",
        "A stranded astronaut discovers an alien civilization on a distant planet."
    ]
    user_premise = random.choice(random_prompts)
    st.write(f"Surprise Premise: {user_premise}")

# Step 2: Generate story beginnings based on the premise
if user_premise:
    st.header("Step 2: Choose a Beginning")
    api_key = st.text_input("🔑 Enter WorqHat API Key:", type="password")

    if st.button("Generate Beginnings"):
        prompt = f"Create the beginning of a story based on this premise: {user_premise}"
        story_data = generate_story(api_key, prompt, "beginning")

        if story_data:
            beginnings = story_data.get('content', {}).get('options', [])
            selected_beginning = st.radio("Choose a beginning:", beginnings)

            if selected_beginning:
                st.write(f"Selected Beginning: {selected_beginning}")
                current_story = selected_beginning

# Step 3: Generate middle parts based on the selected beginning
if 'current_story' in locals():
    st.header("Step 3: Choose a Middle Part")

    if st.button("Generate Middles"):
        prompt = f"Create the middle part of a story based on this beginning: {current_story}"
        story_data = generate_story(api_key, prompt, "middle")

        if story_data:
            middles = story_data.get('content', {}).get('options', [])
            selected_middle = st.radio("Choose a middle part:", middles)

            if selected_middle:
                st.write(f"Selected Middle: {selected_middle}")
                current_story += " " + selected_middle

# Step 4: Generate endings based on the selected middle part
if 'current_story' in locals() and selected_middle:
    st.header("Step 4: Choose an Ending")

    if st.button("Generate Endings"):
        prompt = f"Create the ending of a story based on this storyline: {current_story}"
        story_data = generate_story(api_key, prompt, "end")

        if story_data:
            endings = story_data.get('content', {}).get('options', [])
            selected_ending = st.radio("Choose an ending:", endings)

            if selected_ending:
                st.write(f"Selected Ending: {selected_ending}")
                current_story += " " + selected_ending
                st.success("🎉 Your story is complete!")
                st.markdown(f"### Final Story:\n{current_story}")

# Footer
st.markdown(
    "For more information, visit the [Documentation page](https://docs.worqhat.com) and the [API Reference page](https://docs.worqhat.com/api-9378105)."
)
