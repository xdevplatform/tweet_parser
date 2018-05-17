# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from tweet_parser.tweet_checking import is_original_format
from tweet_parser.getter_methods.tweet_text import get_tweet_type


def get_quoted_tweet(tweet):
    """
    Get the quoted Tweet and return it as a dictionary
    If the Tweet is not a quote Tweet, return None

    Args:
        tweet (Tweet or dict): A Tweet object or a dictionary

    Returns:
        dict: A dictionary representing the quoted status
        or None if there is no quoted status. \n
        - For original format, this is the value of "quoted_status" \n
        - For activity streams, this is the value of "twitter_quoted_status"
    """
    if get_tweet_type(tweet) == "quote":
        if is_original_format(tweet):
            return tweet["quoted_status"]
        else:
            return tweet["twitter_quoted_status"]

    else:
        return None


def get_retweeted_tweet(tweet):
    """
    Get the retweeted Tweet and return it as a dictionary
    If the Tweet is not a Retweet, return None

    Args:
        tweet (Tweet or dict): A Tweet object or a dictionary

    Returns:
        dict: A dictionary representing the retweeted status
        or None if there is no quoted status. \n
        - For original format, this is the value of "retweeted_status" \n
        - For activity streams, If the Tweet is a Retweet this is the value of the key "object"
    """
    if get_tweet_type(tweet) == "retweet":
        if is_original_format(tweet):
            return tweet["retweeted_status"]
        else:
            return tweet["object"]
    else:
        return None


def get_embedded_tweet(tweet):
    """
    Get the retweeted Tweet OR the quoted Tweet and return it as a dictionary

    Args:
        tweet (Tweet): A Tweet object (not simply a dict)

    Returns:
        dict (or None, if the Tweet is neither a quote tweet or a Retweet):
        a dictionary representing the quote Tweet or the Retweet
    """
    if tweet.retweeted_tweet is not None:
        return tweet.retweeted_tweet
    elif tweet.quoted_tweet is not None:
        return tweet.quoted_tweet
    else:
        return None
