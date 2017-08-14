from tweet_parser.tweet_checking import is_original_format


def get_user_mentions(tweet):
    """
    Get the @-mentions in the Tweet as dictionaries.
    Note that in the case of a quote-tweet, this does not return the users
    mentioned in the quoted status. The recommended way to get that list would
    be to use get_user_mentions on the quoted status.
    Also note that in the caes of a quote-tweet, the list of @-mentioned users
    does not include the user who authored the original (quoted) Tweet.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (list of dicts): 1 item per @ mention. Note that the fields here
        aren't enforced by the parser, they are simply the fields as they
        appear in a Tweet data payload.

    Example:


    Example:
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "entities": {"user_mentions": [{
        ...                              "indices": [14,26], #characters where the @ mention appears
        ...                              "id_str": "2382763597", #id of @ mentioned user as a string
        ...                              "screen_name": "notFromShrek", #screen_name of @ mentioned user
        ...                              "name": "Fiona", #display name of @ mentioned user
        ...                              "id": 2382763597 #id of @ mentioned user as an int
        ...                            }]
        ...                          }
        ...             }
        >>> get_user_mentions(original)
        ... {"indices": [14,26],"id_str": "2382763597","screen_name": "notFromShrek","name": "Fiona","id": 2382763597}
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    if tweet[entities]["user_mentions"] is not None:
        return tweet[entities]["user_mentions"]
    else:
        return []


def get_hashtags(tweet):
    """
    Get a list of hashtags in the Tweet
    Note that in the case of a quote-tweet, this does not return the
    hashtags in the quoted status.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (a list of strings): list of all of the hashtags in the Tweet

    Example:
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...            "entities": {"hashtags": [{"text":"1hashtag"}]}}
        >>> get_hashtags(original)
        ["1hashtag"]

        >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...             "twitter_entities": {"hashtags": [
        ...                     {"text":"1hashtag"},
        ...                     {"text": "moreHashtags"}]}}
        >>> get_hashtags(activity)
        ["1hashtag", "moreHashtags"]
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    if tweet[entities]["hashtags"] is not None:
        return [x["text"] for x in tweet[entities]["hashtags"]]
    else:
        return []
