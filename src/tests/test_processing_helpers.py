from assignment import processing_helpers
from test_case import return_test_case_list
import pytest
import pandas as pd

TEST_TWEETS = return_test_case_list()


@pytest.fixture
def test_tweets():
    """ Sample list of tweets as a fixture

    Returns:
        list: list of tweets
    """
    return return_test_case_list()


@pytest.fixture
def search_string():
    """Simulates a search string entered

    Returns:
        string: search term
    """
    return "#kahoot"


def test_clean_tweets(test_tweets, search_string):
    """Tests the clean tweets function

    Args:
        test_tweets (list): list of tweets
        search_string (string): search term
    """
    assert(processing_helpers.clean_tweets(
        test_tweets[18]['full_text'],
        search_string)) == "future engineers scientists participated callisto space innovation amazonfutureengineer atemis donorschoose"


def test_return_users_dataframe(test_tweets):
    """Tests the most common users found

    Args:
        test_tweets (list): list of tweets
    """
    assert(processing_helpers.return_users_dataframe(
        test_tweets)[0][4] == "smnbereisland")


def test_get_most_frequent_tokens(test_tweets, search_string):
    """Test the most frequent terms extracted

    Args:
        test_tweets (list): list of tweets
        search_string (string): search term
    """
    assert(processing_helpers.get_most_frequent_tokens(
        test_tweets, search_string)[0][0] == "fun")
    assert(processing_helpers.get_most_frequent_tokens(
        test_tweets, search_string)[0][1] == "today")
    assert(processing_helpers.get_most_frequent_tokens(
        test_tweets, search_string)[0][2] == "played")


def test_calculate_sentiment(test_tweets):
    """Tests the calculate_sentiment function

    Args:
        test_tweets (list): list of tweets
    """
    tweets_df = pd.DataFrame(test_tweets)
    assert(processing_helpers.calculate_sentiment(
        tweets_df).sentiment_class[0] == "Negative")
    assert(processing_helpers.calculate_sentiment(
        tweets_df).sentiment_class[1] == "Neutural")
    assert(processing_helpers.calculate_sentiment(
        tweets_df).sentiment_class[3] == "Positive")
