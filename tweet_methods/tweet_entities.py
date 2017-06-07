from tweet_methods.tweet_checking import is_original_format

def get_user_mentions(tweet):
    """
    get a list of @ mention dicts from the tweet
    """
    if is_original_format(tweet):
        entities = "entities"
    else:
        entities = "twitter_entities"
    return [x for x in tweet[entities]["user_mentions"]]

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

