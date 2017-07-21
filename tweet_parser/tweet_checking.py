from tweet_parser.tweet_parser_errors import NotATweetError, UnexpectedFormatError
from tweet_parser.tweet_keys import original_format_minimum_set_keys, original_format_superset_keys, activity_streams_minimum_set_keys, activity_streams_superset_keys


def is_original_format(tweet):
    """
    helper function to categorize the format of a tweet
    """
    if hasattr(tweet, "original_format"):
        return tweet.original_format
    else:
        if "created_at" in tweet:
            original_format = True
        elif "postedTime" in tweet:
            original_format = False
        else:
            raise(NotATweetError("This text has neither 'created_at' or 'postedTime' as keys, it's not a Tweet"))
    return original_format


def get_all_keys(tweet, parent_key=''):
    """
    helper function to get all of the keys in a Tweet dictionary
    """
    items = []
    for k, v in tweet.items():
        new_key = parent_key + " " + k
        if isinstance(v, dict):
            items.extend(get_all_keys(v, parent_key=new_key))
        else:
            items.append(new_key.strip(" "))
    return items


def check_format(tweet_keys_list, superset_keys, minset_keys):
    """
    this format checks to see if a Tweet has all of the expected keys (and no unexpected ones)
    """
    # check for changing keys
    # check for keys that must be present
    tweet_keys = set(tweet_keys_list)
    minset_overlap = tweet_keys & minset_keys
    if not (minset_overlap == minset_keys):
        raise(UnexpectedFormatError("Some keys ({}) are missing from your Tweet (note that Public API data is not supported)".format(minset_keys - tweet_keys)))
    # check for keys that could be present
    unexpected_keys = tweet_keys - superset_keys
    if len(unexpected_keys) > 0:
        raise(UnexpectedFormatError("Some unexpected keys ({}) are in your Tweet".format(unexpected_keys)))
    return 0


def check_tweet(tweet, do_format_checking=False):
    # get the format of the Tweet & make sure it's probably a Tweet
    original_format = is_original_format(tweet)
    # make sure, to the best of our knowledge, that the Tweet is a Tweet
    if "id" not in tweet:
        raise(NotATweetError("This text has no 'id' key, it's probably not a Tweet"))
    if original_format:
        # check to see if it's not a Tweet at all
        if "user" not in tweet:
            raise(NotATweetError("This text has no 'user' key, it's probably not a Tweet"))
        if "text" not in tweet:
            raise(NotATweetError("This text has no 'text' key, it's probably not a Tweet"))
        # check for changing keys
        if do_format_checking:
            check_format(get_all_keys(tweet), original_format_superset_keys, original_format_minimum_set_keys)
    else:
        # check to see if it's not a Tweet at all
        if "actor" not in tweet:
            raise(NotATweetError("This text has no 'actor' key, it's probably not a Tweet"))
        if "body" not in tweet:
            raise(NotATweetError("This text has no 'body' key, it's probably not a Tweet"))
        #check for changing keys
        if do_format_checking:
            check_format(get_all_keys(tweet), activity_streams_superset_keys, activity_streams_minimum_set_keys)
    return original_format
