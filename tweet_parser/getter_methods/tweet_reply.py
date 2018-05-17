# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from tweet_parser.tweet_checking import is_original_format
from tweet_parser.tweet_parser_errors import NotAvailableError


def get_in_reply_to_screen_name(tweet):
    """
    Get the screen name of the user whose Tweet is being replied to, None
    if this Tweet is not a reply

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the screen name of the user whose Tweet is being replied to
        (None if not a reply)

    Example:
        >>> from tweet_parser.getter_methods.tweet_reply import *
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "in_reply_to_screen_name": "notFromShrek"
        ...            }
        >>> get_in_reply_to_screen_name(original_format_dict)
        'notFromShrek'

        >>> activity_streams_format_dict = {
        ...         "postedTime": "2017-05-24T20:17:19.000Z",
        ...         "inReplyTo":
        ...            {"link": "http://twitter.com/notFromShrek/statuses/863566329168711681"}
        ...         }
        >>> get_in_reply_to_screen_name(activity_streams_format_dict)
        'notFromShrek'
    """

    if is_original_format(tweet):
        return tweet["in_reply_to_screen_name"]
    else:
        if tweet.get("inReplyTo", None) is not None:
            return tweet["inReplyTo"]["link"].split("/")[-3]
        else:
            return None


def get_in_reply_to_user_id(tweet):
    """
    Get the user id of the uesr whose Tweet is being replied to, and None
    if this Tweet is not a reply. \n
    Note that this is unavailable in activity-streams format

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the user id of the user whose Tweet is being replied to, None
        (if not a reply), or for activity-streams raise a NotAvailableError

    Example:
        >>> from tweet_parser.getter_methods.tweet_reply import *
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "in_reply_to_user_id_str": "2382763597"
        ...            }
        >>> get_in_reply_to_user_id(original_format_dict)
        '2382763597'
    """

    if is_original_format(tweet):
        return tweet["in_reply_to_user_id_str"]
    else:
        raise NotAvailableError("Gnip activity-streams format does not" +
                                " return the replied to user's id")


def get_in_reply_to_status_id(tweet):
    """
    Get the tweet id of the Tweet being replied to, None
    if this Tweet is not a reply

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the tweet id of the Tweet being replied to
        (None if not a reply)

    Example:
        >>> from tweet_parser.getter_methods.tweet_reply import *
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "in_reply_to_status_id_str": "863566329168711681"
        ...            }
        >>> get_in_reply_to_status_id(original_format_dict)
        '863566329168711681'

        >>> activity_streams_format_dict = {
        ...         "postedTime": "2017-05-24T20:17:19.000Z",
        ...         "inReplyTo":
        ...            {"link": "http://twitter.com/notFromShrek/statuses/863566329168711681"}
        ...         }
        >>> get_in_reply_to_status_id(activity_streams_format_dict)
        '863566329168711681'
    """
    if is_original_format(tweet):
        return tweet["in_reply_to_status_id_str"]
    else:
        if tweet.get("inReplyTo", None) is not None:
            return tweet["inReplyTo"]["link"].split("/")[-1]
        else:
            return None
