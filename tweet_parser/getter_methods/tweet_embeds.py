from tweet_parser.tweet_checking import is_original_format


def get_quote_tweet(tweet):
    """
    get the quote Tweet and return the dict
    """
    if tweet.tweet_type == "quote":
        if is_original_format(tweet):
            return tweet["quoted_status"]
        else:
            return tweet["twitter_quoted_status"]

    else:
        return None


def get_retweet(tweet):
    """
    get the retweet and return the dict
    """
    if tweet.tweet_type == "retweet":
        if is_original_format(tweet):
            return tweet["retweeted_status"]
        else:
            return tweet["object"]
    else:
        return None


def get_embedded_tweet(tweet):
    """
    get any embedded Tweet and return the dict
    """
    if tweet.retweet is not None:
        return tweet.retweet
    elif tweet.quote_tweet is not None:
        return tweet.quote_tweet
    else:
        return None
