"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random
import re
import os

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components
import streamlit_analytics

from worqai import Worqhat  # Import the corrected Worqhat class

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Define functions
def generate_text(topic: str, mood: str = ""):
    """Generate Tweet text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.tweet = ""
    st.session_state.image = ""
    st.session_state.text_error = ""

    if not topic:
        st.session_state.text_error = "Please enter a topic"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your Tweet is being generated..."):
            mood_prompt = f"{mood} " if mood else ""
            prompt = f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters:\n\n"

            # Create Worqhat object with the API key from session state
            worqhat = Worqhat(api_key=st.session_state.api_key)
            mood_output = f", Mood: {mood}" if mood else ""
            st.session_state.text_error = ""
            st.session_state.n_requests += 1
            streamlit_analytics.start_tracking()
            tweet = worqhat.complete(prompt=prompt)
            st.session_state.tweet = (
               tweet['content']
            )
            print("The tweet state is ", st.session_state.tweet)
            logging.info(
                f"Topic: {topic}{mood_output}\n"
                f"Tweet: {st.session_state.tweet}"
            )

def generate_image(prompt: str):
    """Generate Tweet image."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another text or image."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    with image_spinner_placeholder:
        with st.spinner("Please wait while your image is being generated..."):
            # Create Worqhat object with the API key from session state
            worqhat = Worqhat(api_key=st.session_state.api_key)
            prompt_wo_hashtags = re.sub("#[A-Za-z0-9_]+", "", prompt)
            processing_prompt = (
                "Create a detailed but brief description of an image that captures "
                f"the essence of the following text:\n{prompt_wo_hashtags}\n\n"
            )
            processed_prompt = (
                worqhat.complete(
                    prompt=processing_prompt, temperature=0.5, max_tokens=40
                )
                
            )
            st.session_state.n_requests += 1
            image_fetch=worqhat.image(processed_prompt)
            print(image_fetch)
            st.session_state.image = image_fetch['image']
            logging.info(f"Tweet: {prompt}\nImage prompt: {processed_prompt}")

# Configure Streamlit page and state
st.set_page_config(page_title="Tweet", page_icon="🤖")

if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "image" not in st.session_state:
    st.session_state.image = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render Streamlit page
streamlit_analytics.start_tracking()
st.title("Generate Tweets")
st.markdown(
    "This mini-app generates Tweets using WorqHat's [LLMs](https://www.worqhat.com/ai) for texts and images. You can find the code on [GitHub](https://github.com/ and the author on [Twitter](https://twitter.com/)."
)

st.session_state.api_key = st.text_input(label="Worqhat API Key", placeholder="Enter your Worqhat API Key")

topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
mood = st.text_input(
    label="Mood (e.g. inspirational, funny, serious) (optional)",
    placeholder="inspirational",
)
col1, col2 = st.columns(2)
with col1:
    st.button(
        label="Generate text",
        type="primary",
        on_click=generate_text,
        args=(topic, mood),  # API key is now in session state
    )
with col2:
    with open("moods.txt") as f:
        sample_moods = f.read().splitlines()
    st.button(
        label="Feeling lucky",
        type="secondary",
        on_click=generate_text,
        args=(random.choice(["A random famous person quote", "A random news headline", "A random funny joke"]), random.choice(sample_moods)),  # API key is now in session state
    )

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.tweet:
    st.markdown("""---""")
    st.text_area(label="Tweet", value=st.session_state.tweet, height=100)
    col1, col2 = st.columns(2)
    with col1:
        components.html(
            f"""
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
""",
            height=45,
        )
    with col2:
        pass # Removed the post tweet button

    # Display the image generated below the generate image button
    if not st.session_state.image:
        st.button(
            label="Generate image",
            type="primary",
            on_click=generate_image,
            args=[st.session_state.tweet],  # API key is now in session state
        )
    else:
        st.image(st.session_state.image)
        st.button(
            label="Regenerate image",
            type="secondary",
            on_click=generate_image,
            args=[st.session_state.tweet],  # API key is now in session state
        )

    image_spinner_placeholder = st.empty()
    if st.session_state.image_error:
        st.error(st.session_state.image_error)

    st.markdown("""---""")

streamlit_analytics.stop_tracking()
