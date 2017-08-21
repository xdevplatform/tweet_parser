from tweet_parser.tweet_checking import is_original_format
from tweet_parser.tweet_parser_errors import NotAvailableError
import re


def get_full_text(tweet):
    """
    Get the full text of a tweet dict.
    Includes @-mention replies and long links.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: the untruncated text of a Tweet
        (finds extended text if available)

    Example:
        >>> from tweet_parser.getter_methods.tweet_text import get_full_text
        >>> # getting the text of a Tweet that is not truncated
        >>> original_untruncated = {
        ...                 "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...                 "truncated": False,
        ...                 "text": "some tweet text"
        ...                }
        >>> get_full_text(original_untruncated)
        'some tweet text'

        >>> activity_untruncated = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...                         "body": "some tweet text"
        ...                        }
        >>> get_full_text(activity_untruncated)
        'some tweet text'

        >>> # getting the text of a truncated Tweet (has over 140 chars)
        >>> original_truncated = {
        ...               "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...               "text": "some tweet text, lorem ip...",
        ...               "truncated": True,
        ...               "extended_tweet":
        ...                 {"full_text":
        ...                   "some tweet text, lorem ipsum dolor sit amet"}
        ...               }
        >>> get_full_text(original_truncated)
        'some tweet text, lorem ipsum dolor sit amet'

        >>> activity_truncated = {
        ...               "postedTime": "2017-05-24T20:17:19.000Z",
        ...               "body": "some tweet text, lorem ip...",
        ...               "long_object":
        ...                 {"body":
        ...                   "some tweet text, lorem ipsum dolor sit amet"}
        ...              }
        >>> get_full_text(activity_truncated)
        'some tweet text, lorem ipsum dolor sit amet'
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
        >>> from tweet_parser.getter_methods.tweet_text import get_text
        >>> original = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "text": "some tweet text"}
        >>> get_text(original)
        'some tweet text'

        >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...             "body": "some tweet text"}
        >>> get_text(activity)
        'some tweet text'
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
        str: (one of 3 strings)
        "tweet": an original Tweet
        "retweet": a native retweet (created with the retweet button)
        "quote": a native quote tweet (etweet button + adding quote text)

    Caveats:
        When a quote-tweet (tweet A) is quote-tweeted (tweet B),
        the innermost quoted tweet (A) in the payload (for B)
        no longer has the key "quoted_status" or "twitter_quoted_status",
        and that tweet (A) would be labeled as a "tweet" (not a "quote").
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


def get_lang(tweet):
    """
    Get the language that the Tweet is written in.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: 2-letter BCP 47 language code (or None if undefined)

    Example:
        >>> from tweet_parser.getter_methods.tweet_text import get_lang
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "lang": "en"}
        >>> get_lang(original)
        'en'

        >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...             "twitter_lang": "en"}
        >>> get_lang(activity)
        'en'
    """
    if is_original_format(tweet):
        lang_field = "lang"
    else:
        lang_field = "twitter_lang"
    if tweet[lang_field] is not None and tweet[lang_field] != "und":
            return tweet[lang_field]
    else:
        return None


def get_poll_options(tweet):
    """
    Get the text in the options of a poll as a list
    - If there is no poll in the Tweet, return an empty list
    - If the Tweet is in activity-streams format, raise 'NotAvailableError'

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list: list of strings, or, in the case where there is no poll,
        an empty list

    Raises:
        NotAvailableError for activity-streams format

    Example:
        >>> from tweet_parser.getter_methods.tweet_text import get_poll_options
        >>> original = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "entities": {"polls": [{"options": [{"text":"a"},
        ...                                                 {"text":"b"},
        ...                                                 {"text":"c"}]
        ...                             }]},
        ...            }
        >>> get_poll_options(original)
        ['a', 'b', 'c']

        >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...             "body": "some tweet text"}
        >>> get_poll_options(activity)
        Traceback (most recent call last):
        ...
        NotAvailableError: Gnip activity-streams format does not return poll options
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
        raise NotAvailableError("Gnip activity-streams format does not" +
                                " return poll options")


def get_quote_or_rt_text(tweet):
    """
    Get the quoted or retweeted text in a Tweet
    (this is not the text entered by the posting user)
    - tweet: empty string (there is no quoted or retweeted text)
    - quote: only the text of the quoted Tweet
    - retweet: the text of the retweet

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        str: text of the retweeted-tweet or the quoted-tweet
        (empty string if this is an original Tweet)

    Example:
        >>> from tweet_parser.getter_methods.tweet_text import get_quote_or_rt_text
        >>> # a quote tweet
        >>> quote = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...          "text": "adding my own commentary",
        ...          "truncated": False,
        ...          "quoted_status": {
        ...                 "created_at": "Mon May 01 05:00:05 +0000 2017",
        ...                 "truncated": False,
        ...                 "text": "an interesting Tweet"
        ...                }
        ...         }

        >>> get_quote_or_rt_text(quote)
        'an interesting Tweet'
    """
    tweet_type = get_tweet_type(tweet)
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
    Helper function to remove the links from the input text

    Args:
        text (str): A string

    Returns:
        str: the same text, but with any substring that matches the regex
        for a link removed and replaced with a space

    Example:
        >>> from tweet_parser.getter_methods.tweet_text import remove_links
        >>> text = "lorem ipsum dolor https://twitter.com/RobotPrincessFi"
        >>> remove_links(text)
        'lorem ipsum dolor  '
    """
    tco_link_regex = re.compile("https?://t.co/[A-z0-9].*")
    generic_link_regex = re.compile("(https?://)?(\w*[.]\w+)+([/?=&]+\w+)*")
    remove_tco = re.sub(tco_link_regex, " ", text)
    remove_generic = re.sub(generic_link_regex, " ", remove_tco)
    return remove_generic
