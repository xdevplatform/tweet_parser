def get_user_id(tweet_dict, is_original_format):
    """
    get the user id, as a string
    """
    if is_original_format:
        return tweet_dict["user"]["id_str"]
    else:
        return tweet_dict["actor"]["id"].split(":")[-1]

def get_screen_name(tweet_dict, is_original_format):
    """
    get the user screen name (@ handle)
    """
    if is_original_format:
        return tweet_dict["user"]["screen_name"]
    else:
        return tweet_dict["actor"]["preferredUsername"]

def get_name(tweet_dict, is_original_format):
    """
    get the user's display name
    """
    if is_original_format:
        return tweet_dict["user"]["name"]
    else:
        return tweet_dict["actor"]["displayName"]
