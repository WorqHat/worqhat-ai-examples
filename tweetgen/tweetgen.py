import streamlit as st
import requests
import json
import random
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="📝 Interactive Story Generator", page_icon="🤖")
st.title("Generate Tweets")
st.markdown(
    "This mini-app generates Tweets using WorqHat's AI for texts and images. You can find the code on [GitHub](https://github.com/kinosal/tweet) and the author on [Twitter](https://twitter.com/kinosal)."
)

worqhat_api_key = st.sidebar.text_input('WorqHat API Key')

def generate_response(input_text, mood):
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": input_text,
        "training_data": f"Write a Tweet about {input_text} in less than 120 characters and in a {mood} tone.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    headers = {
        "Authorization": f"Bearer {worqhat_api_key}",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        st.write("API Response:", response_data)  # Print the API response for debugging
        content = response_data['content']
        content_json = json.loads(content)
        response_text = content_json['tweet']  # Use the correct key 'tweet'
        st.info(response_text)  # Display the response from WorqHat

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.write("Response content:", response.text)

def generate_image(prompt):
    url = "https://api.worqhat.com/api/ai/content/v4"
    payload = {
        "question": prompt,
        "training_data": "Generate an image based on the provided text.",
        "response_type": "json",
        "model": "aicon-v4-nano-160824",
    }
    headers = {
        "Authorization": f"Bearer {worqhat_api_key}",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        st.write("API Response:", response_data)  # Print the API response for debugging
        content = response_data['content']
        content_json = json.loads(content)
        image_url = content_json['imageUrl']
        st.image(image_url)  # Display the image from WorqHat

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.write("Response content:", response.text)

# Configure Streamlit page and state
if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "image" not in st.session_state:
    st.session_state.image = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

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
topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
moods = ["happy", "sad", "angry", "excited", "thoughtful"]
selected_mood = st.selectbox("Mood", moods)
col1, col2 = st.columns(2)
with col1:
    st.button(
        label="Generate text",
        type="primary",
        on_click=generate_response,
        args=(topic, selected_mood),
    )
with col2:
    st.button(
        label="Feeling lucky",
        type="secondary",
        on_click=generate_response,
        args=("an interesting topic", random.choice(moods)),
    )

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
        st.button(
            label="Regenerate text",
            type="secondary",
            on_click=generate_response,
            args=(topic, selected_mood),
        )

    if not st.session_state.image:
        st.button(
            label="Generate image",
            type="primary",
            on_click=generate_image,
            args=[st.session_state.tweet],
        )
    else:
        st.image(st.session_state.image)
        st.button(
            label="Regenerate image",
            type="secondary",
            on_click=generate_image,
            args=[st.session_state.tweet],
        )

    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**"
        )
        st.markdown("[Twitter Wrapped](https://twitter-likes.streamlit.app)")
        st.markdown("[Content Summarizer](https://web-summarizer.streamlit.app)")
        st.markdown("[Code Translator](https://english-to-code.streamlit.app)")
        st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")
    with col2:
        st.write("If you like this app, please consider to")
        components.html(
            """
                <form action="https://www.paypal.com/donate" method="post" target="_top">
                <input type="hidden" name="hosted_button_id" value="8JJTGY95URQCQ" />
                <input type="image" src="https://pics.paypal.com/00/s/MDY0MzZhODAtNGI0MC00ZmU5LWI3ODYtZTY5YTcxOTNlMjRm/file.PNG" height="35" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
                <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
                </form>
            """,
            height=45,
        )
        st.write("so I can keep it alive. Thank you!")
