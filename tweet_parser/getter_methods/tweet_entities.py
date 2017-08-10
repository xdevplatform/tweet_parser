from tweet_parser.tweet_checking import is_original_format


def get_user_mentions(tweet):
    """
    get a list of @ mention dicts from the tweet
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    if tweet[entities]["user_mentions"] is not None:
        return tweet[entities]["user_mentions"]
    else:
        return []


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


def get_hashtags(tweet):
    """
    get a list of hashtags
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    if tweet[entities]["user_mentions"] is not None:
        return [x["text"] for x in tweet[entities]["hashtags"]]
    else:
        return []
