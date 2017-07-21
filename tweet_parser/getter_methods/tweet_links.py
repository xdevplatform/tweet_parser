from tweet_parser.tweet_checking import is_original_format


def get_tweet_links(tweet):
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
        key_mappings = {"expanded_url": "url", "expanded_status": "status",
                        "expanded_url_title": "title", "expanded_url_description": "description"}
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
    return the most unrolled url present
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
