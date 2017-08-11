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
        fields will be missing.
            {'display_url': the url that shows up in the tweet, possibly truncated,
             'expanded_url': long (expanded) url,
             'indices': [55, 78], # characters where the display link is
             'unwound': {
                'description': description from the linked webpage
                'status': 200,
                'title': title of the webpage,
                'url': long (expanded) url},
             'url': url the tweet directs to, often t.co}
    """
    if is_original_format(tweet):
        # get the urls from the Tweet
        try:
            tweet_urls = tweet["entities"]["urls"]
        except KeyError:
            tweet_urls = []
        # get the urls from the quote-tweet
        if tweet.quote_tweet is not None:
            tweet_urls += tweet.quote_tweet.tweet_links
        # get the urls from the retweet
        if tweet.retweet is not None:
            tweet_urls += tweet.retweet.tweet_links
        return tweet_urls
    else:
        # try to get normal urls
        try:
            tweet_urls = tweet["twitter_entities"]["urls"]
        except KeyError:
            tweet_urls = []
        # get the urls from the quote-tweet
        if tweet.quote_tweet is not None:
            tweet_urls += tweet.quote_tweet.tweet_links
        # get the urls from the retweet
        if tweet.retweet is not None:
            tweet_urls += tweet.retweet.tweet_links
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
    In order of preference for "most unrolled":
    Keys from the dict returned by get_tweet_links (tweet.tweet_links):
        1. "unwound"/"url"
        2. "expanded_url"
        3. "url"

    Args:
        tweet (Tweet): A Tweet object (cannot simply be a dict)

    Returns:
        list (list of strings): a list of the most unrolled url available
    """
    unrolled_urls = []
    for url in tweet.tweet_links:
        if "unwound" in url:
            unrolled_urls.append(url["unwound"]["url"])
        elif "expanded_url" in url:
            unrolled_urls.append(url["expanded_url"])
        else:
            unrolled_urls.append(url["url"])
    return unrolled_urls
