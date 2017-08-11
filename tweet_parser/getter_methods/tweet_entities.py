from tweet_parser.tweet_checking import is_original_format


def get_user_mentions(tweet):
    """
    Get the @-mentions in the Tweet as dictionaries.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (list of dicts): 1 item per @ mention, each item has the fields:
             {
                "indices": [14,26], #characters where the @ mention appears
                "id_str": "2382763597", #id of @ mentioned user as a string
                "screen_name": "notFromShrek", #screen_name of @ mentioned user
                "name": "Fiona", #display name of @ mentioned user
                "id": 2382763597 #id of @ mentioned user as an int
              }
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

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (a list of strings): list of all of the hashtags in the Tweet
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    if tweet[entities]["hashtags"] is not None:
        return [x["text"] for x in tweet[entities]["hashtags"]]
    else:
        return []

# do hashtags in the quoted Tweet get included?

def get_quoted_user(tweet):
    """
    quoted users don't get included in the @ mentions
    which doesn't seem that intuitive, so I'm adding a getter to add them
    """
    if tweet.tweet_type == "quote":
        quoted_status_loc = "quoted_status"
        if not is_original_format(tweet):
            quoted_status_loc = "twitter_quoted_status"
        tweet[quoted_status_loc]
    else:
        return []


def get_quoted_mentions(tweet):
    """
    users mentioned in the quoted Tweet don't get included
    which doesn't seem that intuitive, so I'm adding a getter to add them
    """
    if tweet.tweet_type == "quote":
        quoted_status_loc = "quoted_status"
        if not is_original_format(tweet):
            quoted_status_loc = "twitter_quoted_status"
        return get_user_mentions(tweet[quoted_status_loc])
    else:
        return []


