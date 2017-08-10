from tweet_parser.tweet_checking import is_original_format
from tweet_parser.tweet_parser_errors import NotAvailableError
import re


def get_full_text(tweet):
    """
    get the full text of a tweet dict or of the sub-dict in a quote/RT
    """
    if is_original_format(tweet):
        if tweet["truncated"]:
            return tweet["extended_tweet"]["full_text"]
        else:
            return tweet["text"]
    else:
        if "long_object" in tweet:
            return tweet["long_object"]["body"]
        else:
            return tweet["body"]


def get_text(tweet):
    """
    literally the contents of 'text' or 'body'
    """
    if is_original_format(tweet):
        return tweet["text"]
    else:
        return tweet["body"]


def get_tweet_type(tweet):
    """
    3 options: tweet, quote, and retweet
    """
    if is_original_format(tweet):
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
    if is_original_format(tweet):
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
    tweet_type = tweet.tweet_type
    if tweet_type == "tweet":
        return ""
    if tweet_type == "quote":
        if is_original_format(tweet):
            return get_full_text(tweet["quoted_status"])
        else:
            return get_full_text(tweet["twitter_quoted_status"])
    if tweet_type == "retweet":
        if is_original_format(tweet):
            return get_full_text(tweet["retweeted_status"])
        else:
            return get_full_text(tweet["object"])


def get_all_text(tweet):
    """
    all of the text of the tweet
    Includes @ mentions, long links,
    quote-tweet contents (separated by a newline) & RT contents
    & poll options
    """
    if is_original_format(tweet):
        return "\n".join(filter(None, [tweet.user_entered_text, tweet.quote_or_rt_text, "\n".join(tweet.poll_options)]))
    else:
        return "\n".join(filter(None, [tweet.user_entered_text, tweet.quote_or_rt_text]))


def remove_links(text):
    """
    take some text, remove the links
    """
    tco_link_regex = re.compile("https?://t.co/[A-z0-9].*")
    generic_link_regex = re.compile("\<http.+?\>", re.DOTALL)
    new_text = re.sub(tco_link_regex, " ", text)
    return re.sub(generic_link_regex, " ", new_text)
