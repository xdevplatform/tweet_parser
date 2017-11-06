# -*- coding: utf-8 -*-
"""Tweet counts and related attributes

This module holds attributes related to basic counts on tweets, such as
retweets, favs, and quotes. It is unlikely to be extended.
"""

from tweet_parser.tweet_checking import is_original_format

def get_retweet_count(tweet):
    """
    Gets the retweet count for this tweet.

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_retweet_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597'
        ...          'retweet_count': 2}
        2
    """
    return tweet.get("retweet_count", 0)


def get_favorite_count(tweet):
    """
    Gets the favorite count for this tweet.

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_retweet_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597'
        ...          'favorite_count': 2}
        2
    """
    return tweet.get("favorite_count", 0)


def get_quote_count(tweet):
    """
    Gets the quote count for this tweet.

    Example:
        >>> from tweet_parser.getter_methods.tweet_counts import get_retweet_count
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'id_str': '2382763597'
        ...          'quote_count': 2}
        2
    """
    if is_original_format(tweet):
        return tweet.get("quote_count", 0)
    else:
        print("quote counts are only available in original format")
        raise KeyError
