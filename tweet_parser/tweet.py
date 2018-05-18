# -*- coding: utf-8 -*-
# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
import datetime

from tweet_parser.lazy_property import lazy_property
from tweet_parser.tweet_parser_errors import NotATweetError
from tweet_parser import tweet_checking
from tweet_parser.getter_methods import tweet_date, tweet_user, tweet_counts
from tweet_parser.getter_methods import tweet_text, tweet_geo, tweet_links
from tweet_parser.getter_methods import tweet_entities, tweet_embeds
from tweet_parser.getter_methods import gnip_fields, tweet_generator, tweet_reply


class Tweet(dict):
    """
    Tweet object created from a dictionary representing a Tweet paylaod

    Args:
        tweet_dict (dict): A dictionary representing a Tweet payload
        do_format_checking (bool): If "True", compare the keys in this \
        dict to a supeset of expected keys and to a minimum set of expected \
        keys (as defined in tweet_parser.tweet_keys). \
        Will cause the parser to fail if unexpected keys are present \
        or if expected keys are missing. \
        Intended to allow run-time format testing, allowing the user \
        to surface unexpected format changes.

    Returns:
        Tweet: Class "Tweet", inherits from dict, provides properties to
        get various data values from the Tweet.

    Raises:
        NotATweetError: the Tweet dict is malformed, \
        see `tweet_checking.check_tweet` for details

    Example:
        >>> from tweet_parser.tweet import Tweet
        >>> # python dict representing a Tweet
        >>> tweet_dict = {"id": 867474613139156993,
        ...               "id_str": "867474613139156993",
        ...               "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...               "text": "Some Tweet text",
        ...               "user": {
        ...                   "screen_name": "RobotPrincessFi",
        ...                   "id_str": "815279070241955840"
        ...                   }
        ...              }
        >>> # create a Tweet object
        >>> tweet = Tweet(tweet_dict)
        >>> # use the Tweet obj to access data elements
        >>> tweet.id
        '867474613139156993'
        >>> tweet.created_at_seconds
        1495657039
    """
    def __init__(self, tweet_dict, do_format_validation=False):
        """
        Initialize a Tweet object from a dict representing a Tweet payload
        """

        # get the format of the Tweet data
        # also, this throws an error if it's not a tweet
        self.original_format = tweet_checking.check_tweet(tweet_dict,
                                                          do_format_validation)

        # make sure that this obj has all of the keys that our dict had
        self.update(tweet_dict)

    @lazy_property
    def id(self):
        """
        Tweet snowflake id as a string

        Returns:
            str: Twitter snowflake id, numeric only (no other text)

        Example:
            >>> from tweet_parser.tweet import Tweet
            >>> original_format_dict = {
            ...     "created_at": "Wed May 24 20:17:19 +0000 2017",
            ...     "id": 867474613139156993,
            ...     "id_str": "867474613139156993",
            ...     "user": {"user_keys":"user_data"},
            ...     "text": "some tweet text"
            ...     }
            >>> Tweet(original_format_dict).id
            '867474613139156993'

            >>> activity_streams_dict = {
            ...     "postedTime": "2017-05-24T20:17:19.000Z",
            ...     "id": "tag:search.twitter.com,2005:867474613139156993",
            ...     "actor": {"user_keys":"user_data"},
            ...     "body": "some tweet text"
            ...     }
            >>> Tweet(activity_streams_dict).id
            '867474613139156993'
        """
        if self.original_format:
            return self["id_str"]
        else:
            return self["id"].split(":")[-1]

    @lazy_property
    def created_at_seconds(self):
        """
        Time that a Tweet was posted in seconds since the Unix epoch

        Returns:
            int: seconds since the unix epoch
            (determined by converting Tweet.id
            into a timestamp using `tweet_date.snowflake2utc`)
        """
        return tweet_date.snowflake2utc(self.id)

    @lazy_property
    def created_at_datetime(self):
        """
        Time that a Tweet was posted as a Python datetime object

        Returns:
            datetime.datetime: the value of `tweet.created_at_seconds`
            converted into a datetime object
        """
        return datetime.datetime.utcfromtimestamp(self.created_at_seconds)

    @lazy_property
    def created_at_string(self):
        """
        Time that a Tweet was posted as a string with the format
        YYYY-MM-ddTHH:MM:SS.000Z

        Returns:
            str: the value of `tweet.created_at_seconds`
            converted into a string (YYYY-MM-ddTHH:MM:SS.000Z)
        """
        return self.created_at_datetime.strftime("%Y-%M-%dT%H:%M:%S.000Z")

    @lazy_property
    def user_id(self):
        """
        The Twitter ID of the user who posted the Tweet

        Returns:
            str: value returned by calling `tweet_user.get_user_id` on `self`
        """
        return tweet_user.get_user_id(self)

    @lazy_property
    def screen_name(self):
        """
        The screen name (@ handle) of the user who posted the Tweet

        Returns:
            str: value returned by calling `tweet_user.get_screen_name` on `self`
        """
        return tweet_user.get_screen_name(self)

    @lazy_property
    def name(self):
        """
        The display name of the user who posted the Tweet

        Returns:
            str: value returned by calling `tweet_user.get_name` on `self`
        """
        return tweet_user.get_name(self)

    @lazy_property
    def bio(self):
        """
        The bio text of the user who posted the Tweet

        Returns:
            str: the user's bio text.
            value returned by calling `tweet_user.get_bio` on `self`
        """
        return tweet_user.get_bio(self)

    @lazy_property
    def follower_count(self):
        """
        The number of followers that the author of the Tweet has

        Returns:
            int: the number of followers.
            value returned by calling `get_follower_count` on `self`
        """
        return tweet_user.get_follower_count(self)

    @lazy_property
    def following_count(self):
        """
        The number of accounts that the author of the Tweet is following

        Returns:
            int: the number of accounts that the author of the Tweet is following,
            value returned by calling `get_following_count` on `self`
        """
        return tweet_user.get_following_count(self)

    @lazy_property
    def klout_score(self):
        """
        (DEPRECATED): 
        The Klout score (int) (if it exists) of the user who posted the Tweet

        Returns:
            int: value returned by calling `tweet_user.get_klout_score` on `self`
            (if no Klout is present, this returns a None)
        """
        return tweet_user.get_klout_score(self)

    @lazy_property
    def klout_profile(self):
        """
        (DEPRECATED): 
        The Klout profile URL of the user (`str`) (if it exists)

        Returns:
            str: value returned by calling `tweet_user.get_klout_profile` on `self`
            (if no Klout is present, this returns a `None`)
        """
        return tweet_user.get_klout_profile(self)

    @lazy_property
    def klout_id(self):
        """
        (DEPRECATED): 
        The Klout ID of the user (`str`) (if it exists)

        Returns:
            str: value returned by calling `tweet_user.get_klout_id` on `self`
            (if no Klout is present, this returns a `None`)
        """
        return tweet_user.get_klout_id(self)

    @lazy_property
    def klout_influence_topics(self):
        """
        (DEPRECATED): 
        Get the user's Klout influence topics (a list of dicts), if it exists.
        Topic dicts will have these keys: `url`, `id`, `name`, `score`

        Returns:
            list: value returned by calling
            `tweet_user.get_klout_topics(self, topic_type = 'influence')`
            (if no Klout is present, this returns a `None`)
        """
        return tweet_user.get_klout_topics(self, topic_type='influence')

    @lazy_property
    def klout_interest_topics(self):
        """
        (DEPRECATED): 
        Get the user's Klout interest topics (a list of dicts), if it exists.
        Topic dicts will have these keys: `url`, `id`, `name`, `score`

        Returns:
            list: value returned by calling
            `tweet_user.get_klout_topics(self, topic_type = 'interest')`
            (if no Klout is present, this returns a `None`)
        """
        return tweet_user.get_klout_topics(self, topic_type='interest')

    @lazy_property
    def text(self):
        """
        The contents of "text" (original format)
        or "body" (activity streams format)

        Returns:
            str: value returned by calling `tweet_text.get_text` on `self`
        """
        return tweet_text.get_text(self)

    @lazy_property
    def tweet_type(self):
        """
        The type of Tweet this is (3 options: tweet, quote, and retweet)

        Returns:
            str: ("tweet","quote" or "retweet" only)
            value returned by calling `tweet_text.get_tweet_type` on `self`
        """
        return tweet_text.get_tweet_type(self)

    @lazy_property
    def user_entered_text(self):
        """
        The text that the posting user entered \n
        *tweet*: untruncated (includes @-mention replies and long links)
        text of an original Tweet \n
        *quote tweet*: untruncated poster-added content in a quote-tweet \n
        *retweet*: empty string

        Returns:
            str: if `tweet.tweet_type == "retweet"`, returns an empty string
            else, returns the value of `tweet_text.get_full_text(self)`
        """
        if self.tweet_type == "retweet":
            return ""
        return tweet_text.get_full_text(self)

    @lazy_property
    def lang(self):
        """
        The language that the Tweet is written in.

        Returns:
            str: 2-letter BCP 47 language code (or None if undefined)
            Value returned by calling `tweet_text.get_lang` on `self`
        """
        return tweet_text.get_lang(self)

    @lazy_property
    def poll_options(self):
        """
        The text in the options of a poll as a list. \
        If there is no poll in the Tweet, return an empty list. \
        If activity-streams format, raise `NotAvailableError`

        Returns:
            list (list of strings): value returned by calling
            `tweet_text.get_poll_options` on `self`
        """
        return tweet_text.get_poll_options(self)

    @lazy_property
    def quote_or_rt_text(self):
        """
        The quoted or retweeted text in a Tweet
        (this is not the text entered by the posting user) \n
        - tweet: empty string (there is no quoted or retweeted text) \n
        - quote: only the text of the quoted Tweet \n
        - retweet: the text of the retweet

        Returns:
            str: value returned by calling
            tweet_text.get_quote_or_rt_text on `self`
        """
        return tweet_text.get_quote_or_rt_text(self)

    @lazy_property
    def all_text(self):
        """
        All of the text of the tweet. This includes @ mentions, long links,
        quote-tweet contents (separated by a newline), RT contents
        & poll options

        Returns:
            str: value returned by calling `tweet_text.get_all_text` on `self`
        """
        return tweet_text.get_all_text(self)

    @lazy_property
    def geo_coordinates(self):
        """
        The user's geo coordinates, if they are included in the payload
        (otherwise return `None`).
        Dictionary with the keys "latitude" and "longitude" or `None`

        Returns:
            dict: value returned by calling `tweet_geo.get_geo_coordinates` on `self`
        """
        return tweet_geo.get_geo_coordinates(self)

    @lazy_property
    def profile_location(self):
        """
        User's derived location data from the profile location enrichment
        If unavailable, returns `None`.

        Returns:
            dict: value returned by calling tweet_geo.get_profile_location on `self`

        Example:
            >>> result = {"country": "US",         # Two letter ISO-3166 country code
            ...           "locality": "Boulder",   # The locality location (~ city)
            ...           "region": "Colorado",    # The region location (~ state/province)
            ...           "sub_region": "Boulder", # The sub-region location (~ county)
            ...           "full_name": "Boulder, Colorado, US", # The full name (excluding sub-region)
            ...           "geo":  [40,-105]        # lat/long value that coordinate that corresponds to
            ...                                     # the lowest granularity location for where the user
            ...                                     # who created the Tweet is from
            ... }
        """
        return tweet_geo.get_profile_location(self)

    @lazy_property
    def tweet_links(self):
        """
        The links that are included in the Tweet as "urls"
        (if there are no links, this is an empty list)
        This includes links that are included in quoted or retweeted Tweets
        Returns unrolled or expanded_url information if it is available

        Returns:
            list (list of dicts): A list of dictionaries containing information
            about urls. Each dictionary entity can have these keys; without
            unwound url or expanded url Twitter data enrichments many of these
            fields will be missing.
            (value returned by calling tweet_links.get_tweet_links on `self`)

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
        return tweet_links.get_tweet_links(self)

    @lazy_property
    def most_unrolled_urls(self):
        """
        For each url included in the Tweet "urls", get the most unrolled
        version available. Only return 1 url string per url in tweet.tweet_links
        In order of preference for "most unrolled"
        (keys from the dict at tweet.tweet_links): \n
        1. `unwound`/`url` \n
        2. `expanded_url` \n
        3. `url`

        Returns:
            list (a list of strings): list of urls
            value returned by calling tweet_links.get_most_unrolled_urls on `self`
        """
        return tweet_links.get_most_unrolled_urls(self)

    @lazy_property
    def user_mentions(self):
        """
        The @-mentions in the Tweet as dictionaries.
        Note that in the case of a quote-tweet, this does not return the users
        mentioned in the quoted status. The recommended way to get that list
        would be to use 'tweet.quoted_tweet.user_mentions'.
        Also note that in the caes of a quote-tweet, the list of @-mentioned
        users does not include the user who authored the original (quoted) Tweet,
        you can get the author of the quoted tweet using
        `tweet.quoted_tweet.user_id`

        Returns:
            list (list of dicts): 1 item per @ mention,
            value returned by calling `tweet_entities.get_user_mentions` on `self`

        Example:
            >>> result = {
            ...   #characters where the @ mention appears
            ...   "indices": [14,26],
            ...   #id of @ mentioned user as a string
            ...   "id_str": "2382763597",
            ...   #screen_name of @ mentioned user
            ...   "screen_name": "notFromShrek",
            ...   #display name of @ mentioned user
            ...   "name": "Fiona",
            ...   #id of @ mentioned user as an int
            ...   "id": 2382763597
            ... }

        """
        return tweet_entities.get_user_mentions(self)

    @lazy_property
    def hashtags(self):
        """
        A list of hashtags in the Tweet.
        Note that in the case of a quote-tweet, this does not return the
        hashtags in the quoted status. The recommended way to get that list
        would be to use `tweet.quoted_tweet.hashtags`

        Returns:
            list (a list of strings): list of all of the hashtags in the Tweet
            value returned by calling `tweet_entities.get_hashtags` on `self`
        """
        return tweet_entities.get_hashtags(self)

    @lazy_property
    def media_urls(self):
        """
        A list of all media (https) urls in the tweet, useful for grabbing
        photo/video urls for other purposes.

        Returns:
            list (a list of strings): list of all of the media urls in the Tweet
            value returned by calling `tweet_entities.get_media_urls` on `self`
        """
        return tweet_entities.get_media_urls(self)

    @lazy_property
    def quoted_tweet(self):
        """
        The quoted Tweet as a Tweet object
        If the Tweet is not a quote Tweet, return None
        If the quoted Tweet payload cannot be loaded as a Tweet, this will
        raise a "NotATweetError"

        Returns:
            Tweet: A Tweet representing the quoted status (or None)
            (see tweet_embeds.get_quote_tweet, this is that value as a Tweet)

        Raises:
            NotATweetError: if quoted tweet is malformed
        """
        quote_tweet = tweet_embeds.get_quoted_tweet(self)
        if quote_tweet is not None:
            try:
                return Tweet(quote_tweet)
            except NotATweetError as nate:
                raise(NotATweetError("The quote-tweet payload appears malformed." +
                                     " Failed with '{}'".format(nate)))
        else:
            return None

    @lazy_property
    def retweeted_tweet(self):
        """
        The retweeted Tweet as a Tweet object
        If the Tweet is not a Retweet, return None
        If the Retweet payload cannot be loaded as a Tweet, this will
        raise a `NotATweetError`

        Returns:
            Tweet: A Tweet representing the retweeted status (or None)
            (see tweet_embeds.get_retweet, this is that value as a Tweet)

        Raises:
            NotATweetError: if retweeted tweet is malformed
        """
        retweet = tweet_embeds.get_retweeted_tweet(self)
        if retweet is not None:
            try:
                return Tweet(retweet)
            except NotATweetError as nate:
                raise(NotATweetError("The retweet payload appears malformed." +
                                     " Failed with '{}'".format(nate)))
        else:
            return None

    @lazy_property
    def embedded_tweet(self):
        """
        Get the retweeted Tweet OR the quoted Tweet and return it as a Tweet object

        Returns:
            Tweet (or None, if the Tweet is neither a quote tweet or a Retweet):
            a Tweet representing the quote Tweet or the Retweet
            (see tweet_embeds.get_embedded_tweet, this is that value as a Tweet)

        Raises:
            NotATweetError: if embedded tweet is malformed
        """
        embedded_tweet = tweet_embeds.get_embedded_tweet(self)
        if embedded_tweet is not None:
            try:
                return Tweet(embedded_tweet)
            except NotATweetError as nate:
                raise(NotATweetError("The embedded tweet payload {} appears malformed." +
                                     " Failed with '{}'".format(embedded_tweet, nate)))
        else:
            return None

    @lazy_property
    def gnip_matching_rules(self):
        """
        Get the Gnip tagged rules that this tweet matched.

        Returns:
            List of potential tags with the matching rule or None if no rules
            are defined.

        """
        return gnip_fields.get_matching_rules(self)

    @lazy_property
    def generator(self):
        """
        Get information about the application that generated the Tweet

        Returns:
            dict: keys are 'link' and 'name', the link to and name of the application
            that generated the Tweet.
            value returned by calling `tweet_generator.get_generator` on `self`
        """
        return tweet_generator.get_generator(self)

    @lazy_property
    def in_reply_to_screen_name(self):
        """
        The screen name of the user being replied to (None if the Tweet isn't a reply)

        Returns:
            str: value returned by calling `tweet_reply.get_in_reply_to_screen_name` on `self`
        """
        return tweet_reply.get_in_reply_to_screen_name(self)

    @lazy_property
    def in_reply_to_user_id(self):
        """
        The user id of the user being replied to (None if the Tweet isn't a reply).
        This raises a NotAvailableError for activity-streams format

        Returns:
            str: value returned by calling `tweet_reply.get_in_reply_to_user_id` on `self`
        """
        return tweet_reply.get_in_reply_to_user_id(self)

    @lazy_property
    def in_reply_to_status_id(self):
        """
        The status id of the Tweet being replied to (None if the Tweet isn't a reply)

        Returns:
            str: value returned by calling `tweet_reply.get_in_reply_to_status_id` on `self`
        """
        return tweet_reply.get_in_reply_to_status_id(self)

    @lazy_property
    def favorite_count(self):
        """
        The number of favorites that this tweet has received *at the time of
        retrieval*. If a tweet is obtained from a live stream, this will likely
        be 0.

        Returns:
            int: value returned by calling `tweet_counts.get_favorite_count` on `self`
        """
        return tweet_counts.get_favorite_count(self)

    @lazy_property
    def quote_count(self):
        """
        The number of tweets that this tweet has been quoted in *at the time of
        retrieval*. If a tweet is obtained from a live stream, this will likely
        be 0.
        This raises a NotAvailableError for activity-streams format
        
        Returns:
            int: value returned by calling `tweet_counts.get_quote_count` on `self` 
            or raises NotAvailableError
        """
        return tweet_counts.get_quote_count(self)

    @lazy_property
    def retweet_count(self):
        """
        The number of times this tweet has been retweeted *at the time of
        retrieval*. If a tweet is obtained from a live stream, this will likely
        be 0.
        
        Returns:
            int: value returned by calling `tweet_counts.get_retweet_count` on `self` 
        """
        return tweet_counts.get_retweet_count(self)
