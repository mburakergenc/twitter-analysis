"""
This helper module contains helper functions to do several data processing tasks
including datetime manuplation, data cleaning and sentiment calication
"""

import re
import string
import time
from collections import Counter
from datetime import datetime as dt
from datetime import timedelta, timezone

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

STOP_WORDS = stopwords.words()

EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)


def handle_index_error(function):
    """ The decorator that handles common exceptions when data is not available

    Args:
        function (function): function to be checked for IndexError
    """
    def handle_problems(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
            return res
        except (IndexError, AttributeError, KeyError):
            print("No tweets or accounts have been found for the given timeframe")
    return handle_problems


def count_tweets(tweets, minutes):
    """    
    Converts current timezone to UTC
    Compares current time against the tweet's created_at time
    returns matching tweets as a list

    Args:
        tweets (list): list of tweets
        minutes (integer): interval in minutes

    Returns:
        list: list of tweets for the given interval
    """
    tweets_list = []
    current_time_utc = time.mktime(dt.now(timezone.utc).timetuple())
    current_time_minus_interval = time.mktime((
        dt.now(timezone.utc)-timedelta(minutes=minutes)).timetuple())
    for tweet in tweets:
        created_at_tuple = time.mktime(dt.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple())
        if created_at_tuple < current_time_utc and created_at_tuple > current_time_minus_interval:
            tweets_list.append(tweet)

    return tweets_list


def clean_tweets(tweet, search_string):
    """    
    Convert to lowercase.
    Rremove URL links, special characters and punctuation.
    Tokenize and remove stop words.

    Args:
        tweet (dict): Single tweets
        search_string (string): _description_

    Returns:
        dict: cleaned tweet
    """
    tweet = tweet.lower()
    tweet = re.sub(r'https?://\S+|www\.\S+', '', tweet)
    tweet = re.sub(r'<.*?>+', '', tweet)
    tweet = re.sub(r'[%s]' % re.escape(string.punctuation), '', tweet)
    tweet = re.sub(r'\n', '', tweet)
    tweet = re.sub(r'[’“”…]', '', tweet)

    tweet = EMOJI_PATTERN.sub(r'', tweet)

    search_string = search_string.replace("#", "")

    # removing the stop-words
    text_tokens = word_tokenize(tweet)
    tokens_without_sw = [
        word for word in text_tokens if not word in STOP_WORDS if word != search_string]
    filtered_sentence = (" ").join(tokens_without_sw)
    tweet = filtered_sentence

    return tweet


@handle_index_error
def get_most_frequent_tokens(tweets_dict, search_string):
    """
    Converts tweets dictionary into a dataframe
    Cleans the tweets
    Calculates the most common 10 tokens

    Args:
        tweets_dict (list): list of tweets
        search_string (string): search term

    Returns:
        DataFrame: Most common 10 frequent terms
    """
    df_tweets = pd.DataFrame(tweets_dict)
    dt_tweets = df_tweets.full_text.apply(
        clean_tweets, search_string=search_string)
    word_count = Counter(" ".join(dt_tweets).split()).most_common(10)

    return pd.DataFrame(word_count)


@handle_index_error
def return_users_dataframe(counter_object):
    """
    Returns the most active 10 accounts for a given list of tweets

    Args:
        counter_object (List): List of tweets that are counted with the count_tweets() function

    Returns:
        DataFrame: Top 10 most active users
    """
    return pd.DataFrame(Counter(d['screen_name'] for d in pd.DataFrame(counter_object).user).most_common(10))


@handle_index_error
def calculate_sentiment(df_sentiments):
    """   
     Uses TextBlob's sentiment polarity to detect the sentiment
     returns a dataframe with the sentiment score and sentiment class

    Args:
        df_sentiments (DataFrame): Tweets DataFrame

    Returns:
        DataFrame: Tweet, sentiment score, and sentiment class
    """

    text = df_sentiments["full_text"]

    for i in range(0, len(text)):

        text_blob = TextBlob(text[i])

        sentiment_score = text_blob.sentiment.polarity

        df_sentiments.at[i, 'sentiment_score'] = sentiment_score

        if sentiment_score < 0.00:

            sentiment_class = 'Negative'

            df_sentiments.at[i, 'sentiment_class'] = sentiment_class

        elif sentiment_score > 0.00:

            sentiment_class = 'Positive'

            df_sentiments.at[i, 'sentiment_class'] = sentiment_class

        else:

            sentiment_class = 'Neutural'

            df_sentiments.at[i, 'sentiment_class'] = sentiment_class

    return df_sentiments[["full_text", "sentiment_score", "sentiment_class"]]
