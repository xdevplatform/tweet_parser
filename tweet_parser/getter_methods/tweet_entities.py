# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from tweet_parser.tweet_checking import is_original_format
from tweet_parser.getter_methods.tweet_embeds import get_retweeted_tweet
from tweet_parser.getter_methods.tweet_text import get_tweet_type

def get_entities(tweet):
    """
    Helper function to simply grabbing the entities. \n
    Caveat: In the case of Retweets, a Retweet is stored as
    "RT @someone: Some awesome status". In the case where pre-appending
    the string "RT @someone:" causes the Tweet to exceed 140 characters,
    entites (hashtags, mentions, urls) beyond the 140 character mark are
    excluded from the Retweet's entities. This seems like counterintuitive
    behavior, so we ensure here that the entities of a Retweet are a
    superset of the entities of the Retweeted status.

    Args:
        tweet (Tweet or dict): Tweet in question

    Returns:
        dict: dictionary of potential entities.

    Example:
        >>> from tweet_parser.getter_methods.tweet_entities import get_entities
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "entities": {"user_mentions": [{
        ...                              "indices": [14,26], #characters where the @ mention appears
        ...                              "id_str": "2382763597", #id of @ mentioned user as a string
        ...                              "screen_name": "notFromShrek", #screen_name of @ mentioned user
        ...                              "name": "Fiona", #display name of @ mentioned user
        ...                              "id": 2382763597 #id of @ mentioned user as an int
        ...                            }]
        ...                          }
        ...             }
        >>> get_entities(original)
        {'user_mentions': [{'indices': [14, 26], 'id_str': '2382763597', 'screen_name': 'notFromShrek', 'name': 'Fiona', 'id': 2382763597}]}
        """

    entity_key = "entities" if is_original_format(tweet) else "twitter_entities"
    if get_tweet_type(tweet) == "retweet":
        retweet_entities = tweet.get(entity_key, [])
        all_entities = get_retweeted_tweet(tweet).get(entity_key,[]).copy()
        # the only thing that the Retweet will have that the Retweeted Tweet
        # won't have is the @-mention of the RTd user at the front ("RT @someone:")
        # I'm going to add that in, so the the Retweet's entities are a superset
        # of the RTd Tweet's entites
        all_entities["user_mentions"] = ([retweet_entities["user_mentions"][0]] +
            all_entities["user_mentions"])
        return all_entities
    else:
        return tweet.get(entity_key, [])


def get_media_entities(tweet):
    """
    Grabs all the media entities from a tweet, which are contained in the
    "extended_entities" or "twitter_extended_entities" field depending on the
    tweet format. Note that this is not the same as the first media entity from
    the basic `entities` key; this is required to get *all* of the potential
    media contained within a tweet. This is useful as an entry point for other
    functions or for any custom parsing that needs to be done.

    Args:
        tweet (Tweet or dict): the tweet in question

    Returns:
        list or None: the list of dicts containing each media's metadata in the
        tweet.

    Example:
        >>> from tweet_parser.getter_methods.tweet_entities import get_media_entities
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'entities': {'user_mentions': [{'id': 2382763597,
        ...          'id_str': '2382763597',
        ...          'indices': [14, 26],
        ...          'name': 'Fiona',
        ...          'screen_name': 'notFromShrek'}]},
        ...          'extended_entities': {'media': [{'display_url': 'pic.twitter.com/something',
        ...          'expanded_url': 'https://twitter.com/something',
        ...          'id': 4242,
        ...          'id_str': '4242',
        ...          'indices': [88, 111],
        ...          'media_url': 'http://pbs.twimg.com/media/something.jpg',
        ...          'media_url_https': 'https://pbs.twimg.com/media/something.jpg',
        ...          'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600},
        ...          'medium': {'h': 799, 'resize': 'fit', 'w': 1200},
        ...          'small': {'h': 453, 'resize': 'fit', 'w': 680},
        ...          'thumb': {'h': 150, 'resize': 'crop', 'w': 150}},
        ...          'type': 'photo',
        ...          'url': 'https://t.co/something'},
        ...          {'display_url': 'pic.twitter.com/something_else',
        ...          'expanded_url': 'https://twitter.com/user/status/something/photo/1',
        ...          'id': 4243,
        ...          'id_str': '4243',
        ...          'indices': [88, 111],
        ...          'media_url': 'http://pbs.twimg.com/media/something_else.jpg',
        ...          'media_url_https': 'https://pbs.twimg.com/media/something_else.jpg',
        ...          'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600},
        ...          'medium': {'h': 799, 'resize': 'fit', 'w': 1200},
        ...          'small': {'h': 453, 'resize': 'fit', 'w': 680},
        ...          'thumb': {'h': 150, 'resize': 'crop', 'w': 150}},
        ...          'type': 'photo',
        ...          'url': 'https://t.co/something_else'}]}
        ...         }
        >>> get_media_entities(tweet)
        [{'display_url': 'pic.twitter.com/something', 'expanded_url': 'https://twitter.com/something', 'id': 4242, 'id_str': '4242', 'indices': [88, 111], 'media_url': 'http://pbs.twimg.com/media/something.jpg', 'media_url_https': 'https://pbs.twimg.com/media/something.jpg', 'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600}, 'medium': {'h': 799, 'resize': 'fit', 'w': 1200}, 'small': {'h': 453, 'resize': 'fit', 'w': 680}, 'thumb': {'h': 150, 'resize': 'crop', 'w': 150}}, 'type': 'photo', 'url': 'https://t.co/something'}, {'display_url': 'pic.twitter.com/something_else', 'expanded_url': 'https://twitter.com/user/status/something/photo/1', 'id': 4243, 'id_str': '4243', 'indices': [88, 111], 'media_url': 'http://pbs.twimg.com/media/something_else.jpg', 'media_url_https': 'https://pbs.twimg.com/media/something_else.jpg', 'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600}, 'medium': {'h': 799, 'resize': 'fit', 'w': 1200}, 'small': {'h': 453, 'resize': 'fit', 'w': 680}, 'thumb': {'h': 150, 'resize': 'crop', 'w': 150}}, 'type': 'photo', 'url': 'https://t.co/something_else'}]
    """

    ext_ents_key = "extended_entities" if is_original_format(tweet) else "twitter_extended_entities"
    ext_ents = tweet.get(ext_ents_key)
    media = ext_ents.get("media", []) if ext_ents else []
    return media


def get_media_urls(tweet):
    """
    Gets the https links to each media entity in the tweet.

    Args:
        tweet (Tweet or dict): tweet

    Returns:
        list: list of urls. Will be an empty list if there are no urls present.

    Example:
        >>> from tweet_parser.getter_methods.tweet_entities import get_media_urls
        >>> tweet = {'created_at': '2017-21-23T15:21:21.000Z',
        ...          'entities': {'user_mentions': [{'id': 2382763597,
        ...          'id_str': '2382763597',
        ...          'indices': [14, 26],
        ...          'name': 'Fiona',
        ...          'screen_name': 'notFromShrek'}]},
        ...          'extended_entities': {'media': [{'display_url': 'pic.twitter.com/something',
        ...          'expanded_url': 'https://twitter.com/something',
        ...          'id': 4242,
        ...          'id_str': '4242',
        ...          'indices': [88, 111],
        ...          'media_url': 'http://pbs.twimg.com/media/something.jpg',
        ...          'media_url_https': 'https://pbs.twimg.com/media/something.jpg',
        ...          'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600},
        ...          'medium': {'h': 799, 'resize': 'fit', 'w': 1200},
        ...          'small': {'h': 453, 'resize': 'fit', 'w': 680},
        ...          'thumb': {'h': 150, 'resize': 'crop', 'w': 150}},
        ...          'type': 'photo',
        ...          'url': 'https://t.co/something'},
        ...          {'display_url': 'pic.twitter.com/something_else',
        ...          'expanded_url': 'https://twitter.com/user/status/something/photo/1',
        ...          'id': 4243,
        ...          'id_str': '4243',
        ...          'indices': [88, 111],
        ...          'media_url': 'http://pbs.twimg.com/media/something_else.jpg',
        ...          'media_url_https': 'https://pbs.twimg.com/media/something_else.jpg',
        ...          'sizes': {'large': {'h': 1065, 'resize': 'fit', 'w': 1600},
        ...          'medium': {'h': 799, 'resize': 'fit', 'w': 1200},
        ...          'small': {'h': 453, 'resize': 'fit', 'w': 680},
        ...          'thumb': {'h': 150, 'resize': 'crop', 'w': 150}},
        ...          'type': 'photo',
        ...          'url': 'https://t.co/something_else'}]}
        ...         }
        >>> get_media_urls(tweet)
        ['https://pbs.twimg.com/media/something.jpg', 'https://pbs.twimg.com/media/something_else.jpg']
    """

    media = get_media_entities(tweet)
    urls = [m.get("media_url_https") for m in media] if media else []
    return urls



def get_user_mentions(tweet):
    """
    Get the @-mentions in the Tweet as dictionaries.
    Note that in the case of a quote-tweet, this does not return the users
    mentioned in the quoted status. The recommended way to get that list would
    be to use get_user_mentions on the quoted status.
    Also note that in the caes of a quote-tweet, the list of @-mentioned users
    does not include the user who authored the original (quoted) Tweet.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (list of dicts): 1 item per @ mention. Note that the fields here
        aren't enforced by the parser, they are simply the fields as they
        appear in a Tweet data payload.

    Example:
        >>> from tweet_parser.getter_methods.tweet_entities import get_user_mentions
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "text": "RT @notFromShrek: Stuff! Words! ...",
        ...             "entities": {"user_mentions": [{
        ...                              "indices": [2,12], #characters where the @ mention appears
        ...                              "id_str": "2382763597", #id of @ mentioned user as a string
        ...                              "screen_name": "notFromShrek", #screen_name of @d user
        ...                              "name": "Fiona", #display name of @ mentioned user
        ...                              "id": 2382763597 #id of @ mentioned user as an int
        ...                            }]
        ...                          },
        ...             "retweeted_status": {
        ...                 "created_at": "Wed May 24 20:01:19 +0000 2017",
        ...                 "text": "Stuff! Words! #Tweeting!",
        ...                 "entities": {"user_mentions": []}
        ...                 }
        ...             }
        >>> get_user_mentions(original)
        [{'indices': [2, 12], 'id_str': '2382763597', 'screen_name': 'notFromShrek', 'name': 'Fiona', 'id': 2382763597}]
    """
    entities = get_entities(tweet)
    user_mentions = entities.get("user_mentions") if entities else None
    return user_mentions if user_mentions else []


def get_hashtags(tweet):
    """
    Get a list of hashtags in the Tweet
    Note that in the case of a quote-tweet, this does not return the
    hashtags in the quoted status.

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        list (a list of strings): list of all of the hashtags in the Tweet

    Example:
        >>> from tweet_parser.getter_methods.tweet_entities import get_hashtags
        >>> original = {"created_at": "Wed May 24 20:17:19 +0000 2017",
        ...            "entities": {"hashtags": [{"text":"1hashtag"}]}}
        >>> get_hashtags(original)
        ['1hashtag']

        >>> activity = {"postedTime": "2017-05-24T20:17:19.000Z",
        ...             "verb": "post",
        ...             "twitter_entities": {"hashtags": [
        ...                     {"text":"1hashtag"},
        ...                     {"text": "moreHashtags"}]}}
        >>> get_hashtags(activity)
        ['1hashtag', 'moreHashtags']
    """
    entities = get_entities(tweet)
    hashtags = entities.get("hashtags")
    hashtags = [tag["text"] for tag in hashtags] if hashtags else []
    return hashtags
