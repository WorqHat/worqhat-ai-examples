"""WorqHat API connector."""

# Import from standard library
import os
import logging
import requests

# Import from 3rd party libraries
import streamlit as st

# Instantiate WorqHat API with credentials from environment or streamlit secrets
# worqhat_api_key = 'sk-02e44d2ccb164c738a6c4a65dbf75e89'  # Remove this line
worqhat_api_url = "https://api.worqhat.com/api/ai"

# Suppress WorqHat request/response logging
# Handle by manually changing the respective APIRequestor methods in the WorqHat package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):
logging.getLogger("worqhat").setLevel(logging.WARNING)


class Worqhat:
    """WorqHat API Connector."""

    def __init__(self, api_key: str):
        """Initialize Worqhat object with API key."""
        self.api_key = api_key

    def complete(
        self,
        prompt: str,
        model: str = "aicon-v4-nano-160824",
        temperature: float = 0.9,
        max_tokens: int = 50,
    ) -> str:
        """Call WorqHat GPT Completion with text prompt.
        Args:
            prompt: text prompt
            model: WorqHat model name, e.g. "aicon-v4-nano-160824"
            temperature: float between 0 and 1
            max_tokens: int between 1 and 2048
        Return: predicted response text
        """
        print("The prompt is ", prompt)
        try:
            response = requests.post(
                f"{worqhat_api_url}/content/v4",
                json={
                    "question": prompt,
                    "model": model,
                    "randomness": temperature,
                    "stream_data": False,
                    "training_data": "create a tweet similar to what the prompt, mood and other parameters suggest",
                    "response_type": "text",
                },
                headers={"Authorization": f"Bearer {self.api_key}"},  # Use self.api_key
            )
            response.raise_for_status()
            print("The response from the AI is ", response)
            return response.json()

        except Exception as e:
            logging.error(f"WorqHat API error: {e}")
            st.session_state.text_error = f"WorqHat API error: {e}"

    def image(self, prompt: str) -> str:
        """Call WorqHat Image Create with text prompt.
        Args:
            prompt: text prompt
        Return: image url
        """
        try:
            prompt_send = prompt['content']
            print("The prompt coming is ", prompt_send)
            response = requests.post(
                f"{worqhat_api_url}/images/generate/v3",
                json={
                    "prompt": [prompt_send],
                    "orientation": "Square",
                    "output_type": "url",
                },
                headers={"Authorization": f"Bearer {self.api_key}"},  # Use self.api_key
            )
            response.raise_for_status()
            print("The response from the Image AI ", response)
            return response.json()

        except Exception as e:
            logging.error(f"WorqHat API error: {e}")
            st.session_state.image_error = f"WorqHat API error: {e}"
