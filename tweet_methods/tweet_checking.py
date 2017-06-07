from tweet_methods.tweet_parser_errors import InvalidJSONError, NotATweetError, NotAvailableError

def check_tweet(tweet):
    # get the format of the Tweet & make sure it's probably a Tweet
    if "created_at" in tweet:
        original_format = True
        activity_streams = False
    elif "postedTime" in tweet:
        original_format = False
        activity_streams = True
    else:
        raise(NotATweetError("This text has neither 'created_at' or 'postedTime' as keys, it's probably not a Tweet"))
    # make sure, to the best of our knowledge, that the Tweet is a Tweet
    if "id" not in tweet:
        raise(NotATweetError("This text has no 'id' key, it's probably not a Tweet"))
    if original_format:
        if "user" not in tweet:
            raise(NotATweetError("This text has no 'user' key, it's probably not a Tweet"))
        if "text" not in tweet:
            raise(NotATweetError("This text has no 'text' key, it's probably not a Tweet"))
    else:
        if "actor" not in tweet:
            raise(NotATweetError("This text has no 'actor' key, it's probably not a Tweet"))
        if "body" not in tweet:
            raise(NotATweetError("This text has no 'body' key, it's probably not a Tweet"))
    return (original_format, activity_streams)