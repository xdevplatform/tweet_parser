import re

def get_full_text(tweet_dict, is_original_format = None):
    """
    get the full text of a tweet dict or of the sub-dict in a quote/RT 
    """
    if is_original_format is None:
        original_format = tweet_dict.original_format
    else:
        original_format = is_original_format
    if original_format:
        if tweet_dict["truncated"]:
            return tweet_dict["extended_tweet"]["full_text"]
        else:
            return tweet_dict["text"]
    else:
        if "long_object" in tweet_dict:
            return tweet_dict["long_object"]["body"]
        else:
            return tweet_dict["body"]

def get_text(tweet):
    """
    literally the contents of 'text' or 'body'
    """
    if tweet.original_format:
        return tweet["text"]
    else:
        return tweet["body"]        

def get_tweet_type(tweet):
    """
    3 options: tweet, quote, and retweet
    """
    if tweet.original_format:
        if "retweeted_status" in tweet:
            return "retweet"
        elif "quoted_status" in tweet:
            return "quote"
        else:
            return "tweet"
    else:
        if tweet["verb"] == "share":
            return "retweet"
        else:
            if "twitter_quoted_status" in tweet:
                return "quote"
            else:
                return "tweet"


def get_poll_options(tweet):
    """
    text in the options of a poll, as a list
    """
    if tweet.original_format:
        try:
            poll_options_text = []
            for p in tweet["entities"]["polls"]:
                for o in p["options"]:
                    poll_options_text.append(o["text"])
            return poll_options_text
        except KeyError:
            return []
            
    else:
        raise NotAvailableError("Gnip activity-streams format does not return poll options")

def get_quote_or_rt_text(tweet):
    """
    the text of a quote tweet or a retweet
    """
    tweet_type = get_tweet_type(tweet)
    if tweet_type == "tweet":
        return ""
    if tweet_type == "quote":
        if tweet.original_format:
            return get_full_text(tweet["quoted_status"], True)
        else:
            return get_full_text(tweet["twitter_quoted_status"], False)
    if tweet_type == "retweet":
        if tweet.original_format:
            return get_full_text(tweet["retweeted_status"], True)
        else:
            return get_full_text(tweet["object"], False)   

def get_all_text(self):
    """
    all of the text of the tweet
    Includes @ mentions, long links, 
    quote-tweet contents (separated by a newline) & RT contents
    & poll options
    """
    if self.original_format:
        return "\n".join(filter(None, [self.user_entered_text,self.quote_or_rt_text,"\n".join(self.poll_options)]))
    else:
        return "\n".join(filter(None, [self.user_entered_text,self.quote_or_rt_text]))

def remove_links(text):
    """
    take some text, remove the links
    """
    tco_link_regex = re.compile("https?://t.co/[A-z0-9].*")
    generic_link_regex = re.compile("\<http.+?\>", re.DOTALL)
    new_text = re.sub(tco_link_regex, " ", text)
    return re.sub(generic_link_regex, " ", new_text)

