"""
Main handler module that returns the necessarry data from Twitter based on the assignment
"""
import pandas as pd
from processing_helpers import calculate_sentiment, count_tweets, get_most_frequent_tokens, return_users_dataframe
from tweepy_helpers import search_tweets


if __name__ == '__main__':
    while True:
        search_string = input(
            "Please enter your search term: (q or e to exit)\n").lower()

        if search_string.lower() in {'q', 'quit', 'e', 'exit'}:
            print("Goodbye!")
            break
        tweets = search_tweets(search_string)
        print("Number of tweets returned: {0}".format(len(tweets)))

        tweets_last_60_mins = count_tweets(tweets, 60)
        tweets_last_5_mins = count_tweets(tweets, 5)
        tweets_last_min = count_tweets(tweets, 1)

        print("Tweets in the last hour: {0}".format(len(tweets_last_60_mins)))
        print("Tweets in the last 5 mins: {0}".format(len(tweets_last_5_mins)))
        print("Tweets in the last min: {0}".format(len(tweets_last_min)))

        print("Most frequent terms in the last hour: {0}".format(
            get_most_frequent_tokens(tweets_last_60_mins, search_string)))

        print("Most frequent terms in the last 5 minutes: {0}".format(
            get_most_frequent_tokens(tweets_last_5_mins, search_string)))

        print("Most frequent terms in the last minute: {0}".format(
            get_most_frequent_tokens(tweets_last_min, search_string)))

        print("Most frequent accounts in the last hour:\n{0}".format(
            return_users_dataframe(tweets_last_60_mins)))

        print("Most frequent accounts in the last 5 minutes::\n{0}".format(
            return_users_dataframe(tweets_last_5_mins)))

        print("Most frequent accounts in the last minute:\n{0}".format(
            return_users_dataframe(tweets_last_min)))

        print("Sentiment analysis for the tweets in the last minute:\n{0}".format(
            calculate_sentiment(pd.DataFrame(tweets_last_min))
        ))

        print("Sentiment analysis for the tweets in the last 5 minutes:\n{0}".format(
            calculate_sentiment(pd.DataFrame(tweets_last_5_mins))
        ))

        print("Sentiment analysis for the tweets in the last hour:\n{0}".format(
            calculate_sentiment(pd.DataFrame(tweets_last_60_mins))
        ))
