from tweet_parser.tweet_checking import is_original_format
from tweet_parser.tweet_parser_errors import NotAvailableError
import re


def get_full_text(tweet):
    """
    Get the full text of a tweet dict

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: the untruncated text of a Tweet
             (finds extended text if available)

    Example:
        >>> # getting the text of a Tweet that is not truncated
        >>> original_untruncated = {
                            "created_at": "Wed May 24 20:17:19 +0000 2017",
                            "truncated": False,
                            "text": "some tweet text"
                           }
        >>> get_full_text(original_untruncated)
        "some tweet text"

        >>> activity_untruncated = {"postedTime": "2017-05-24T20:17:19.000Z",
                                    "body": "some tweet text"
                                   }
        >>> get_full_text(activity_untruncated)
        "some tweet text"

        >>> # getting the text of a truncated Tweet (has over 140 chars)
        >>> original_truncated = {
                          "created_at": "Wed May 24 20:17:19 +0000 2017",
                          "text": "some tweet text, lorem ip...",
                          "truncated": True,
                          "extended_tweet":
                            {"full_text":
                              "some tweet text, lorem ipsum dolor sit amet"}
                          }
        >>> get_full_text(original_truncated)
        "some tweet text, lorem ipsum dolor sit amet"

        >>> activity_truncated = {
                          "postedTime": "2017-05-24T20:17:19.000Z",
                          "body": "some tweet text, lorem ip...",
                          "long_object":
                            {"body":
                              "some tweet text, lorem ipsum dolor sit amet"}
                         }
        >>> get_full_text(activity_truncated)
        "some tweet text, lorem ipsum dolor sit amet"
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
    Get the contents of "text" (original format)
    or "body" (activity streams format)

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: the contents of "text" key (original format)
             or "body" key (activity streams format)

    Example:
    >>> original = {
                    "created_at": "Wed May 24 20:17:19 +0000 2017",
                    "text": "some tweet text"
                   }
    >>> get_text(original)
    "some tweet text"

    >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
                    "body": "some tweet text"
                   }
    >>> get_text(activity)
    "some tweet text"
    """
    if is_original_format(tweet):
        return tweet["text"]
    else:
        return tweet["body"]


def get_tweet_type(tweet):
    """
    Get the type of Tweet this is (3 options: tweet, quote, and retweet)

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: one of 3 strings:
             "tweet": an original Tweet
             "retweet": a native retweet (created with the retweet button)
             "quote": a native quote tweet (created with retweet button
                                            + adding quote text)

    Caveats: When a quote-tweet (tweet A) is quote-tweeted (tweet B),
             the innermost quoted tweet (A) in the payload (for B)
             no longer has the key "quoted_status" or "twitter_quoted_status",
             and that tweet (A) would be labeled as a "tweet" (not a "quote")
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
    Get the text in the options of a poll, as a list.
    If there is no poll in the Tweet, return an empty list.

    Args:

    Returns:
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
    Get the text of a quote tweet or a retweet
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
    Get all of the text of the tweet. This includes @ mentions, long links,
    quote-tweet contents (separated by a newline), RT contents & poll options

    Args:
        tweet (Tweet): A Tweet object (must be a Tweet object)

    Returns:
        str: text from tweet.user_entered_text, tweet.quote_or_rt_text and
             tweet.poll_options (if in original format), separated by newlines
    """
    if is_original_format(tweet):
        return "\n".join(filter(None, [tweet.user_entered_text,
                                       tweet.quote_or_rt_text,
                                       "\n".join(tweet.poll_options)]))
    else:
        return "\n".join(filter(None, [tweet.user_entered_text,
                                       tweet.quote_or_rt_text]))


def remove_links(text):
    """
    Remove the links from the input text

    Args:
        text (str): A string

    Returns:
        str: the same text, but with any substring that matches the regex
             for a link removed and replaced with a space

    Example:
        >>> text = "lorem ipsum dolor https://twitter.com/RobotPrincessFi"
        >>> remove_links(text)
        "lorem ipsum dolor  "
    """
    tco_link_regex = re.compile("https?://t.co/[A-z0-9].*")
    generic_link_regex = re.compile("\<http.+?\>", re.DOTALL)
    new_text = re.sub(tco_link_regex, " ", text)
    return re.sub(generic_link_regex, " ", new_text)
