"""
Helper functions that perform operations on Tweepy to connect to the Twitter API
"""


import tweepy
from credentials import (ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY,
                         CONSUMER_SECRET)


def authenticate_twitter():
    """Authenticates with given credentials in the credentials file

    Returns:
        OAuthHandler: Authenticates with Twitter API details
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth


def search_tweets(search_term):
    """Calls the api.search_tweets endpoint with the given search_term
    Args:
        search_term (string): given search term

    Returns:
        list: list of tweets
    """
    api = tweepy.API(authenticate_twitter(), wait_on_rate_limit=True)
    tweets = tweepy.Cursor(api.search_tweets, tweet_mode="extended", q=search_term +
                           " exclude:retweets ").items(100)
    tweets = [tweet._json for tweet in tweets]

    return tweets
