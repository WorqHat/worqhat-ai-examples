"""Twitter API connector."""

# Import from standard library
import os

# Import from 3rd party libraries
import streamlit as st
import tweepy

# Assign credentials from environment variable or streamlit secrets dict
consumer_key ='AH7t8z6SnSF7MCm7QCOomcns3'
consumer_secret = 'Cv34iYdnqyM3Cod3U2wF8JUBjcH0EVO7Iab6nAfXWljSJNAlML'
access_key = '3239063905-ceBJEqAzTZyQrhGSoD6qs0ZEwGx8VtQOqqG1sZU'
access_secret = 'vifW4m0b8jEWrz8vg1Pz8hW66LnUHAU4HIy9XFgDOjnRA'


class Tweets:
    """Twitter connector."""

    def __init__(self, account):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.account = account

    def fetch_tweets(self) -> list:
        """Fetch most recent tweets."""
        try:
            tweets = self.api.user_timeline(
                screen_name=self.account,
                tweet_mode="extended",  # returns full text
                count=50,
                exclude_replies=True,
                include_rts=False,
            )
            return [tweet.full_text for tweet in tweets][:10]
        except tweepy.errors.NotFound:
            st.error("Twitter account not found.")
        except tweepy.errors.Unauthorized:
            st.error("Twitter account is private.")
        return []
