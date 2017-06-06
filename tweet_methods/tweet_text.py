import re

def get_full_text(tweet_dict, is_original_format):
    if is_original_format:
        if tweet_dict["truncated"]:
            return tweet_dict["extended_tweet"]["full_text"]
        else:
            return tweet_dict["text"]
    else:
        if "long_object" in tweet_dict:
            return tweet_dict["long_object"]["body"]
        else:
            return tweet_dict["body"]

def get_text(tweet_dict, is_original_format):
    """
    literally the contents of 'text' or 'body'
    """
    if is_original_format:
        return tweet_dict["text"]
    else:
        return tweet_dict["body"]        

def get_tweet_type(tweet_dict, is_original_format):
    """
    3 options: tweet, quote, and retweet
    """
    if is_original_format:
        if "retweeted_status" in tweet_dict:
            return "retweet"
        elif "quoted_status" in tweet_dict:
            return "quote"
        else:
            return "tweet"
    else:
        if tweet_dict["verb"] == "share":
            return "retweet"
        else:
            if "twitter_quoted_status" in tweet_dict:
                return "quote"
            else:
                return "tweet"


def get_poll_options(tweet_dict, is_original_format):
    """
    text in the options of a poll, as a list
    """
    if is_original_format:
        try:
            poll_options_text = []
            for p in tweet_dict["entities"]["polls"]:
                for o in p["options"]:
                    poll_options_text.append(o["text"])
            return poll_options_text
        except KeyError:
            return []
            
    else:
        raise NotAvailableError("Gnip activity-streams format does not return poll options")

def get_quote_or_rt_text(tweet_dict, is_original_format):
    """
    the text of a quote tweet or a retweet
    """
    tweet_type = get_tweet_type(tweet_dict, is_original_format)
    if tweet_type == "tweet":
        return ""
    if tweet_type == "quote":
        if is_original_format:
            return get_full_text(tweet_dict["quoted_status"], True)
        else:
            return get_full_text(tweet_dict["twitter_quoted_status"], False)
    if tweet_type == "retweet":
        if is_original_format:
            return get_full_text(tweet_dict["retweeted_status"], True)
        else:
            return get_full_text(tweet_dict["object"], False)   

def remove_links(text):
    """
    take some text, remove the links
    """
    tco_link_regex = re.compile("https?://t.co/[A-z0-9].*")
    generic_link_regex = re.compile("\<http.+?\>", re.DOTALL)
    new_text = re.sub(tco_link_regex, " ", text)
    return re.sub(generic_link_regex, " ", new_text)

