def get_tweet_links(tweet_dict, is_original_format):
    if is_original_format:
        # check if there are urls at all
        try:
            urls = tweet_dict["entities"]["urls"]
        except KeyError:
            return {}
        all_url_info_normalized = {}
        for url in urls:
            all_url_info_normalized[url["url"]] = {}
            if "unwound" in url:
                all_url_info_normalized[url["url"]]["expanded_url"] = url["unwound"]["url"]
                all_url_info_normalized[url["url"]]["expanded_url_title"] = url["unwound"]["title"]
                all_url_info_normalized[url["url"]]["expanded_url_description"] = url["unwound"]["description"]
                all_url_info_normalized[url["url"]]["is_twitter_dot_com"] = "twitter.com" in url["unwound"]["url"] 
            else:
                try:
                    all_url_info_normalized[url["url"]]["expanded_url"] = url["expanded_url"]
                    all_url_info_normalized[url["url"]]["is_twitter_dot_com"] = "twitter.com" in url["expanded_url"]
                except KeyError:
                    pass
        return all_url_info_normalized           
    else:
        # get urls from the gnip enrichment, if it exists
        try:
            gnip_urls = {x["url"]: x for x in tweet_dict["gnip"]["urls"]}
        except KeyError:
            gnip_urls = {}
        # get urls from the twitter entities piece
        try:
            twitter_urls = {x["url"]: x for x in tweet_dict["twitter_entities"]["urls"]}
        except KeyError:
            twitter_urls = {}
        # if there aren't urls, don't do anything else
        all_url_info = {}
        for url in list(gnip_urls.keys()) + list(twitter_urls.keys()):
            all_url_info[url] = {"gnip": gnip_urls.get(url, {}), "twitter": twitter_urls.get(url, {})}
        all_url_info_normalized = {}
        for u in all_url_info:
            url = all_url_info[u]
            all_url_info_normalized[u] = {}
            if url["gnip"]:
                if "expanded_url" in url["gnip"]:
                    all_url_info[u]["url"] = u
                    all_url_info_normalized[u]["expanded_url"] = url["gnip"]["expanded_url"]
                    all_url_info_normalized[u]["expanded_url_title"] = url["gnip"]["expanded_url_title"]
                    all_url_info_normalized[u]["expanded_url_description"] = url["gnip"]["expanded_url_description"]
                    all_url_info_normalized[u]["is_twitter_dot_com"] = "twitter.com" in url["gnip"]["expanded_url"]   
                elif "expanded_url" in url["twitter"]:
                    all_url_info_normalized[u]["url"] = u
                    all_url_info_normalized[u]["expanded_url"] = url["twitter"]["expanded_url"]
                    all_url_info_normalized[u]["is_twitter_dot_com"] = "twitter.com" in url["twitter"]["expanded_url"]                    
            else:
                if "expanded_url" in url["twitter"]:
                    all_url_info_normalized[u]["url"] = u
                    all_url_info_normalized[u]["expanded_url"] = url["twitter"]["expanded_url"]
                    all_url_info_normalized[u]["is_twitter_dot_com"] = "twitter.com" in url["twitter"]["expanded_url"]

        return all_url_info_normalized

def get_most_unrolled_url(url_info):
    """
    return the most unrolled url present
    """
    unrolled_urls = []
    for url in url_info:
        if "expanded_url" in url_info[url]:
            unrolled_urls.append(url_info[url]["expanded_url"])
        else:
            unrolled_urls.append(url_info[url]["url"])
    return unrolled_urls 
