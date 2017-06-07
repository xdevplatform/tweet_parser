def get_user_id(tweet):
    """
    get the user id, as a string
    """
    if tweet.original_format:
        return tweet["user"]["id_str"]
    else:
        return tweet["actor"]["id"].split(":")[-1]

def get_screen_name(tweet):
    """
    get the user screen name (@ handle)
    """
    if tweet.original_format:
        return tweet["user"]["screen_name"]
    else:
        return tweet["actor"]["preferredUsername"]

def get_name(tweet):
    """
    get the user's display name
    """
    if tweet.original_format:
        return tweet["user"]["name"]
    else:
        return tweet["actor"]["displayName"]
