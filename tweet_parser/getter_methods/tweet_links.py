# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from tweet_parser.tweet_checking import is_original_format


def get_tweet_links(tweet):
    """
    Get the links that are included in the Tweet as "urls"
    (if there are no links in the Tweet, this returns an empty list)
    This includes links that are included in quoted or retweeted Tweets
    Returns unrolled or expanded_url information if it is available

    Args:
        tweet (Tweet): A Tweet object (must be a Tweet obj, not a dict)

    Returns:
        list (list of dicts): A list of dictionaries containing information
        about urls. Each dictionary entity can have these keys; without
        unwound url or expanded url Twitter data enrichments many of these
        fields will be missing. \n
        More information about the Twitter url enrichments at:
        http://support.gnip.com/enrichments/expanded_urls.html and
        http://support.gnip.com/enrichments/enhanced_urls.html

    Example:
        >>> result = [
        ...   {
        ...   # url that shows up in the tweet text
        ...   'display_url': "https://twitter.com/RobotPrinc...",
        ...   # long (expanded) url
        ...   'expanded_url': "https://twitter.com/RobotPrincessFi",
        ...   # characters where the display link is
        ...   'indices': [55, 88],
        ...   'unwound': {
        ...      # description from the linked webpage
        ...      'description': "the Twitter profile of RobotPrincessFi",
        ...      'status': 200,
        ...      # title of the webpage
        ...      'title': "the Twitter profile of RobotPrincessFi",
        ...      # long (expanded) url}
        ...      'url': "https://twitter.com/RobotPrincessFi"},
        ...   # the url that tweet directs to, often t.co
        ...   'url': "t.co/1234"}]
    """
    if is_original_format(tweet):
        # get the urls from the Tweet
        try:
            tweet_urls = tweet["entities"]["urls"]
        except KeyError:
            tweet_urls = []
        # get the urls from the quote-tweet
        if tweet.quoted_tweet is not None:
            tweet_urls += tweet.quoted_tweet.tweet_links
        # get the urls from the retweet
        if tweet.retweeted_tweet is not None:
            tweet_urls += tweet.retweeted_tweet.tweet_links
        return tweet_urls
    else:
        # try to get normal urls
        try:
            tweet_urls = tweet["twitter_entities"]["urls"]
        except KeyError:
            tweet_urls = []
        # get the urls from the quote-tweet
        if tweet.quoted_tweet is not None:
            tweet_urls += tweet.quoted_tweet.tweet_links
        # get the urls from the retweet
        if tweet.retweeted_tweet is not None:
            tweet_urls += tweet.retweeted_tweet.tweet_links
        # otherwise, we're now going to combine the urls to try to
        # to get the same format as the og format urls, try to get enriched urls
        try:
            gnip_tweet_urls = {x["url"]: x for x in tweet["gnip"]["urls"]}
            gnip_tweet_exp_urls = {x["expanded_url"]: x for x in tweet["gnip"]["urls"]}
        except KeyError:
            return tweet_urls
        key_mappings = {"expanded_url": "url",
                        "expanded_status": "status",
                        "expanded_url_title": "title",
                        "expanded_url_description": "description"}
        tweet_urls_expanded = []
        for url in tweet_urls:
            expanded_url = url
            if url["url"] in gnip_tweet_urls:
                expanded_url["unwound"] = {key_mappings[key]: value for key, value in gnip_tweet_urls[url["url"]].items() if key != "url"}
            elif url.get("expanded_url", "UNAVAILABLE") in gnip_tweet_exp_urls:
                expanded_url["unwound"] = {key_mappings[key]: value for key, value in gnip_tweet_urls[url["expanded_url"]].items() if key != "url"}
            tweet_urls_expanded.append(expanded_url)
        return tweet_urls_expanded


def get_most_unrolled_urls(tweet):
    """
    For each url included in the Tweet "urls", get the most unrolled
    version available. Only return 1 url string per url in tweet.tweet_links
    In order of preference for "most unrolled"
    (keys from the dict at tweet.tweet_links): \n
    1. `unwound`/`url` \n
    2. `expanded_url` \n
    3. `url`

    Args:
        tweet (Tweet): A Tweet object or dict

    Returns:
        list (list of strings): a list of the most unrolled url available
    """
    unrolled_urls = []
    for url in get_tweet_links(tweet):
        if url.get("unwound", {"url": None}).get("url", None) is not None:
            unrolled_urls.append(url["unwound"]["url"])
        elif url.get("expanded_url", None) is not None:
            unrolled_urls.append(url["expanded_url"])
        else:
            unrolled_urls.append(url["url"])
    return unrolled_urls
