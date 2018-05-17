# -*- coding: utf-8 -*-
# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
"""Tweet counts and related attributes

This module holds attributes related to basic counts on tweets, such as
retweets, favs, and quotes. It is unlikely to be extended.
"""

from tweet_parser.tweet_checking import is_original_format
from tweet_parser.tweet_parser_errors import NotAvailableError

def get_retweet_count(tweet):
    """
    Gets the retweet count for this tweet.

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        int: The number of times the Tweet has been retweeted

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_retweet_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597',
        ...          'retweet_count': 2}
        >>> get_retweet_count(tweet)
        2

        >>> activity_streams_tweet = {'postedTime': '2017-05-24T20:17:19.000Z',
        ...                           'retweetCount': 3}
        >>> get_retweet_count(activity_streams_tweet)
        3
    """
    if is_original_format(tweet):
        return tweet.get("retweet_count", 0)
    else:
        return tweet.get("retweetCount", 0)


def get_favorite_count(tweet):
    """
    Gets the favorite count for this tweet.

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        int: The number of times the Tweet has been favorited

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_favorite_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597',
        ...          'favorite_count': 2}
        >>> get_favorite_count(tweet)
        2
        
        >>> activity_streams_tweet = {'postedTime': '2017-05-24T20:17:19.000Z',
        ...                           'favoritesCount': 3}
        >>> get_favorite_count(activity_streams_tweet)
        3
    """
    if is_original_format(tweet):
        return tweet.get("favorite_count", 0)
    else:
        return tweet.get("favoritesCount", 0)


def get_quote_count(tweet):
    """
    Gets the quote count for this tweet. \n 
    Note that this is unavailable in activity-streams format

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        int: The number of times the Tweet has been quoted
        or for activity-streams raise a NotAvailableError

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_quote_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597',
        ...          'quote_count': 2}
        >>> get_quote_count(tweet)
        2
    """
    if is_original_format(tweet):
        return tweet.get("quote_count", 0)
    else:
        raise NotAvailableError("Quote counts are only available in original format")
