# -*- coding: utf-8 -*-
"""Validation and checking methods for Tweets.

Methods here are primarily used by other methods within this module but can be
used for other validation code as well.
"""

from tweet_parser.tweet_parser_errors import NotATweetError, UnexpectedFormatError
from tweet_parser.tweet_keys import original_format_minimum_set_keys
from tweet_parser.tweet_keys import activity_streams_minimum_set_keys
from tweet_parser.tweet_keys import original_format_superset_keys, activity_streams_superset_keys


def is_original_format(tweet):
    """
    Simple checker to flag the format of a tweet.

    Args:
        tweet (Tweet): tweet in qustion

    Returns:
        Bool

    Example:
        >>> import tweet_parser.tweet_checking as tc
        >>> tweet = {"created_at": 124125125125,
        ...          "text": "just setting up my twttr",
        ...          "nested_field": {"nested_1": "field", "nested_2": "field2"}}
        >>> tc.is_original_format(tweet)
        True
    """
    # deleted due to excess checking; it's a key lookup and does not need any
    # operational optimization
    if "created_at" in tweet:
        original_format = True
    elif "postedTime" in tweet:
        original_format = False
    else:
        raise NotATweetError("This dict has neither 'created_at' or 'postedTime' as keys")
    return original_format


def get_all_keys(tweet, parent_key=''):
    """
    Takes a tweet object and recursively returns a list of all keys contained
    in this level and all nexstted levels of the tweet.

    Args:
        tweet (Tweet): the tweet dict
        parent_key (str): key from which this process will start, e.g., you can
                          get keys only under some key that is not the top-level key.

    Returns:
        list of all keys in nested dicts.

    Example:
        >>> import tweet_parser.tweet_checking as tc
        >>> tweet = {"created_at": 124125125125, "text": "just setting up my twttr",
        ...          "nested_field": {"nested_1": "field", "nested_2": "field2"}}
        >>> tc.get_all_keys(tweet)
        ['created_at', 'text', 'nested_field nested_1', 'nested_field nested_2']
    """
    items = []
    for k, v in tweet.items():
        new_key = parent_key + " " + k
        if isinstance(v, dict):
            items.extend(get_all_keys(v, parent_key=new_key))
        else:
            items.append(new_key.strip(" "))
    return items


def key_validation_check(tweet_keys_list, superset_keys, minset_keys):
    """
    Validates the keys present in a Tweet.

    Args:
        tweet_keys_list (list): the keys present in a tweet
        superset_keys (set): the set of all possible keys for a tweet
        minset_keys (set): the set of minimal keys expected in a tweet.

    Returns:
        0 if no errors

    Raises:
        UnexpectedFormatError on any mismatch of keys.
    """
    # check for keys that must be present
    tweet_keys = set(tweet_keys_list)
    minset_overlap = tweet_keys & minset_keys
    if minset_overlap != minset_keys:
        raise UnexpectedFormatError("keys ({}) missing from Tweet (Public API data is not supported)"
                                    .format(minset_keys - tweet_keys))
    # check for keys that could be present
    unexpected_keys = tweet_keys - superset_keys
    if len(unexpected_keys) > 0:
        raise UnexpectedFormatError("Unexpected keys ({}) are in this Tweet"
                                    .format(unexpected_keys))
    return 0



def _check_original_format_tweet(tweet, validation_checking=False):
    for key in ["user", "text"]:
        if key not in tweet:
            raise NotATweetError("This dict has no '{}' key".format(key))
    # check for changing keys
    if validation_checking:
        _ = key_validation_check(get_all_keys(tweet),
                                 original_format_superset_keys,
                                 original_format_minimum_set_keys)


def _check_activity_streams_tweet(tweet, validation_checking=False):
    for key in ["actor", "body"]:
        if key not in tweet:
            raise NotATweetError("This dict has no '{}' key".format(key))
    # check for changing keys
    if validation_checking:
        _ = key_validation_check(get_all_keys(tweet),
                                 activity_streams_superset_keys,
                                 activity_streams_minimum_set_keys)



def check_tweet(tweet, validation_checking=False):
    """
    Ensures a tweet is valid and determines the type of format for the tweet.

    Args:
        tweet (dict/Tweet): the tweet payload
        validation_checking (bool): check for valid key structure in a tweet.
    """

    if "id" not in tweet:
        raise NotATweetError("This text has no 'id' key")

    original_format = is_original_format(tweet)

    if original_format:
        _check_original_format_tweet(tweet, validation_checking=validation_checking)
    else:
        _check_activity_streams_tweet(tweet, validation_checking=validation_checking)

    return original_format
