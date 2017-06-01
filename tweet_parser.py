import datetime
try:
    import ujson as json
    json_decode_error = ValueError
except ImportError:
    import json
    json_decode_error = json.JSONDecodeError

class cached_property():
    """
    Descriptor (non-data) for building an attribute on-demand on first use.
    https://stackoverflow.com/questions/4037481/caching-attributes-of-classes-in-python
    """
    def __init__(self, factory):
        """
        <factory> is called such: factory(instance) to build the attribute.
        """
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        # Build the attribute.
        attr = self._factory(instance)

        # Cache the value; hide ourselves.
        setattr(instance, self._attr_name, attr)

        return attr

class InvalidJSONError(Exception):
    pass
class NotATweetError(Exception):
    pass
class NotAvailableError(Exception):
    pass


# Twitter Snowflake ID to timestamp (and back)
# https://github.com/client9/snowflake2time/
# Nick Galbreath @ngalbreath nickg@client9.com
# Public Domain -- No Copyright -- Cut-n-Paste!
def snowflake2utc(sf):
    sf_int = int(sf)
    return int(((sf_int >> 22) + 1288834974657) / 1000.0)

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


class tweet():
    """
    tweet class 
    """
    def __init__(self, json_text = None, tweet_dict = None):
        """
        load the JSON formatted text once and store it as a dictionary
        """
        # potentially deal with character encoding issues?
        # TBD
        if json_text is not None:
            # store the original text
            self.original_json = json_text
            # load & store the Tweet as a dict
            try:
                self.tweet_dict = json.loads(json_text)
            except json_decode_error:
                raise InvalidJSONError("Unable to laod JSON text")
        elif tweet_dict is not None:
            self.tweet_dict = tweet_dict
        else:
            raise(NotATweetError("You didn't even pass me anything."))
        # get the format of the Tweet & make sure it's probably a Tweet
        if "created_at" in self.tweet_dict:
            self.activity_streams = False
            self.original_format = True
        elif "postedTime" in self.tweet_dict:
            self.activity_streams = True
            self.original_format = False
        else:
            raise(NotATweetError("This text has neither 'created_at' or 'postedTime' as keys, it's probably not a Tweet"))
        # make sure, to the best of our knowledge, that the Tweet is a Tweet
        if "id" not in self.tweet_dict:
            raise(NotATweetError("This text has no 'id' key, it's probably not a Tweet"))
        if self.original_format:
            if "user" not in self.tweet_dict:
                raise(NotATweetError("This text has no 'user' key, it's probably not a Tweet"))
            if "text" not in self.tweet_dict:
                raise(NotATweetError("This text has no 'text' key, it's probably not a Tweet"))
        else:
            if "actor" not in self.tweet_dict:
                raise(NotATweetError("This text has no 'actor' key, it's probably not a Tweet"))
            if "body" not in self.tweet_dict:
                raise(NotATweetError("This text has no 'body' key, it's probably not a Tweet"))

    
    @cached_property
    def id(self):
        """
        return the Tweet id as a string
        """
        if self.original_format:
            return self.tweet_dict["id_str"]
        else:
            return self.tweet_dict["id"].split(":")[-1]

    @cached_property
    def created_at_seconds(self):
        """
        return seconds since the unix epoch of the Tweet create
        """
        return snowflake2utc(self.id)

    @cached_property
    def created_at_datetime(self):
        """
        return a python datetime obj of the Tweet create
        """
        return datetime.datetime.utcfromtimestamp(self.created_at_seconds)

    @cached_property
    def created_at_string(self):
        """
        return a date string, formatted as: YYYY-MM-ddTHH:MM:SS.000Z
        """
        return self.created_at_datetime.strftime("YYYY-MM-ddTHH:MM:SS.000Z")

    @cached_property
    def user_id(self):
        """
        get the user id, as a string
        """
        if self.original_format:
            return self.tweet_dict["user"]["id_str"]
        else:
            return self.tweet_dict["actor"]["id"].split(":")[-1]

    @cached_property
    def screen_name(self):
        """
        get the user screen name (@ handle)
        """
        if self.original_format:
            return self.tweet_dict["user"]["screen_name"]
        else:
            return self.tweet_dict["actor"]["preferredUsername"]

    @cached_property
    def name(self):
        """
        get the user's display name
        """
        if self.original_format:
            return self.tweet_dict["user"]["name"]
        else:
            return self.tweet_dict["actor"]["displayName"]

    @cached_property
    def text(self):
        """
        literally the contents of 'text' or 'body'
        """
        if self.original_format:
            return self.tweet_dict["text"]
        else:
            return self.tweet_dict["body"]        

    @cached_property
    def tweet_type(self):
        """
        3 options: tweet, quote, and retweet
        """
        if self.original_format:
            if "retweeted_status" in self.tweet_dict:
                return "retweet"
            elif "quoted_status" in self.tweet_dict:
                return "quote"
            else:
                return "tweet"
        else:
            if self.tweet_dict["verb"] == "share":
                return "retweet"
            else:
                if "twitter_quoted_status" in self.tweet_dict:
                    return "quote"
                else:
                    return "tweet"

    @cached_property
    def text(self):
        """
        literally the contents of 'text' or 'body'
        """
        if self.original_format:
            return self.tweet_dict["text"]
        else:
            return self.tweet_dict["body"]

    @cached_property
    def user_entered_text(self):
        """
        text that the actor actually entered 
        not the text of a quote-tweet or the text of a retweet
        all of the text 
        (not truncated, includes @ mention relpies and long links)
        """
        if self.tweet_type == "retweet":
            return ""
        return get_full_text(self.tweet_dict, self.original_format)

    @cached_property
    def poll_options(self):
        """
        text in the options of a poll, as a list
        """
        if self.original_format:
            try:
                poll_options_text = []
                for p in self.tweet_dict["entities"]["polls"]:
                    for o in p["options"]:
                        poll_options_text.append(o["text"])
                return poll_options_text
            except KeyError:
                return []
                
        else:
            raise NotAvailableError("Gnip activity-streams format does not return poll options")

    @cached_property
    def quote_or_rt_text(self):
        """
        the text of a quote tweet or a retweet
        """
        if self.tweet_type == "tweet":
            return ""
        if self.tweet_type == "quote":
            if self.original_format:
                return get_full_text(self.tweet_dict["quoted_status"], True)
            else:
                return get_full_text(self.tweet_dict["twitter_quoted_status"], False)
        if self.tweet_type == "retweet":
            if self.original_format:
                return get_full_text(self.tweet_dict["retweeted_status"], True)
            else:
                return get_full_text(self.tweet_dict["object"], False)          

    @cached_property
    def all_text(self):
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

    @cached_property
    def user_entered_text_without_links(self):
        """
        same as user_entered_text, but links are removed and replaced with __LINK__
        """
        pass

    @cached_property
    def all_text_without_links(self):
        """
        same as all_text, but links are removed and replaced with __LINK__
        """
        pass

    @cached_property
    def geo_coordinates(self):
        """ 
        return the geo coordinates, if they are included in the payload
        else raise 'unavailable field' error
        """
        if "geo" in self.tweet_dict:
            if self.tweet_dict["geo"] is not None:
                if "coordinates" in self.tweet_dict["geo"]:
                    [lat,lon] = self.tweet_dict["geo"]["coordinates"]
                    return {"latitude": lat, "longitude": lon}
        raise(NotAvailableError("Geo coordinates are not included in this Tweet"))

    @cached_property
    def normalized_url_info(self):
        """
        if unrolled urls are availble, return unrolled urls
        if unrolled urls are not availble, return whatever link is availble in entities
        if there are no links, return an empty list
        """
        if self.original_format:
            # check if there are urls at all
            try:
                urls = self.tweet_dict["entities"]["urls"]
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
                gnip_urls = {x["url"]: x for x in self.tweet_dict["gnip"]["urls"]}
            except KeyError:
                gnip_urls = {}
            # get urls from the twitter entities piece
            try:
                twitter_urls = {x["url"]: x for x in self.tweet_dict["twitter_entities"]["urls"]}
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


    @cached_property
    def most_unrolled_url(self):
        """
        return the most unrolled url present
        """
        url_info = self.normalized_url_info
        unrolled_urls = []
        for url in url_info:
            if "expanded_url" in url_info[url]:
                unrolled_urls.append(url_info[url]["expanded_url"])
            else:
                unrolled_urls.append(url_info[url]["url"])
        return unrolled_urls           


### make an importable tweet tokenizer module



