from tweet_parser.tweet_checking import is_original_format


def get_user_id(tweet):
    """
    Get the Twitter ID of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the Twitter ID of the user who posted the Tweet

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_user_id
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"id_str": "815279070241955840"}
        ...            }
        >>> get_user_id(original_format_dict)
        '815279070241955840'

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "actor":
        ...              {"id": "id:twitter.com:815279070241955840"}
        ...             }
        >>> get_user_id(activity_streams_format_dict)
        '815279070241955840'
    """

    if is_original_format(tweet):
        return tweet["user"]["id_str"]
    else:
        return tweet["actor"]["id"].split(":")[-1]


def get_screen_name(tweet):
    """
    Get the screen name (@ handle) of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the @ handle of the user who posted the Tweet

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_screen_name
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"screen_name": "RobotPrincessFi"}
        ...            }
        >>> get_screen_name(original_format_dict)
        'RobotPrincessFi'

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "actor":
        ...              {"preferredUsername": "RobotPrincessFi"}
        ...             }
        >>> get_screen_name(activity_streams_format_dict)
        'RobotPrincessFi'
    """

    if is_original_format(tweet):
        return tweet["user"]["screen_name"]
    else:
        return tweet["actor"]["preferredUsername"]


def get_name(tweet):
    """
    Get the display name of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the @ handle of the user who posted the Tweet

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_name
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"name": "jk no"}
        ...            }
        >>> get_name(original_format_dict)
        'jk no'

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "actor":
        ...              {"displayName": "jk no"}
        ...             }
        >>> get_name(activity_streams_format_dict)
        'jk no'
    """

    if is_original_format(tweet):
        return tweet["user"]["name"]
    else:
        return tweet["actor"]["displayName"]


def get_bio(tweet):
    """
    Get the bio text of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the bio text of the user who posted the Tweet
        In a payload the abscence of a bio seems to be represented by an
        empty string or a None, this getter always returns a string (so, empty
        string if no bio is available).

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_bio
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"description": "Niche millenial content aggregator"}
        ...            }
        >>> get_bio(original_format_dict)
        'Niche millenial content aggregator'

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "actor":
        ...              {"summary": "Niche millenial content aggregator"}
        ...             }
        >>> get_bio(activity_streams_format_dict)
        'Niche millenial content aggregator'
    """

    if is_original_format(tweet):
        return tweet["user"].get("description", "")
    else:
        return tweet["actor"].get("summary", "")


def get_utc_offset(tweet):
    """
    Get the utc offset (if it's available) of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        int: a signed integer indicating the number of seconds offset of the
        user's home timezone from UTC time

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_utc_offset
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"utc_offset": -21600}
        ...            }
        >>> get_utc_offset(original_format_dict)
        -21600

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "actor":
        ...              {"utcOffset": "-21600"}
        ...             }
        >>> get_utc_offset(activity_streams_format_dict)
        -21600
    """

    if is_original_format(tweet):
        return tweet["user"]["utc_offset"]
    else:
        if tweet["actor"]["utcOffset"] is not None:
            return int(tweet["actor"]["utcOffset"])
        else:
            return None


def get_klout_score(tweet):
    """
    Get the Klout score (int) (if it exists) of the user who posted the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        int: the Klout score (if it exists) of the user who posted the Tweet
            else return None

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_klout_score
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "user":
        ...              {"derived": {"klout": {"score": 12345}}}
        ...            }
        >>> get_klout_score(original_format_dict)
        12345

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "gnip":{"klout_score": 12345}}
        >>> get_klout_score(activity_streams_format_dict)
        12345
    """

    try:
        if is_original_format(tweet):
            score = tweet['user']['derived']['klout']['score']
        else:
            score = tweet['gnip']['klout_score']
        return score
    except KeyError:
        return None


def get_klout_profile(tweet):
    """
    Get the Klout profile URL of the user (str) (if it exists)

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the user's Klout profile URL (if it exists), else return None

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_klout_profile
        >>> original_format_dict = {
        ... "created_at": "Wed May 24 20:17:19 +0000 2017",
        ... "user":
        ...     {"derived": {"klout":
        ...         {"profile_url":
        ...             "http://klout.com/topic/id/10000000000000016635"}}}
        ... }
        >>> get_klout_profile(original_format_dict)
        'http://klout.com/topic/id/10000000000000016635'

        >>> activity_streams_format_dict = {
        ... "postedTime": "2017-05-24T20:17:19.000Z",
        ... "gnip":
        ...     {"klout_profile": {
        ...         "link": "http://klout.com/topic/id/10000000000000016635"}
        ...     }
        ... }
        >>> get_klout_profile(activity_streams_format_dict)
        'http://klout.com/topic/id/10000000000000016635'
    """

    try:
        if is_original_format(tweet):
            profile = tweet['user']['derived']['klout']['profile_url']
        else:
            profile = tweet['gnip']['klout_profile']['link']
        return profile
    except KeyError:
        return None


def get_klout_id(tweet):
    """
    Get the Klout ID of the user (str) (if it exists)

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        str: the user's Klout ID (if it exists), else return None

    Example:
        >>> from tweet_parser.getter_methods.tweet_user import get_klout_id
        >>> original_format_dict = {
        ... "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...     "user":
        ...         {"derived": {"klout":
        ...             {"user_id":"1234567890"}}}
        ...     }
        >>> get_klout_id(original_format_dict)
        '1234567890'

        >>> activity_streams_format_dict = {
        ... "postedTime": "2017-05-24T20:17:19.000Z",
        ... "gnip":
        ...     {"klout_profile": {
        ...         "klout_user_id": "1234567890"}
        ...     }}
        >>> get_klout_id(activity_streams_format_dict)
        '1234567890'
    """

    try:
        if is_original_format(tweet):
            klout_id = tweet['user']['derived']['klout']['user_id']
        else:
            klout_id = tweet['gnip']['klout_profile']['klout_user_id']
        return klout_id
    except KeyError:
        return None


def get_klout_topics(tweet, topic_type='influence'):
    """
    Get the user's chosen Klout topics (a list of dicts), if it exists.
    Regardless of format or topic type, topic dicts will have the same keys:
    "url", "id", "name", "score"

    Args:
        tweet (Tweet): A Tweet object
        topic_type (str): Which type of Klout topic to return.
                          Options are limited to 'influence' and 'interest'

    Returns:
        list: A list of dicts representing Klout topics, or if Klout topics \
        do not exist in the Tweet payload, return None. The list is sorted by
        the "score" value.

    Example:
        >>> result = [{
        ...     # the user's score for that topic
        ...     "score": 0.54,
        ...     # the Klout topic ID
        ...     "id": "10000000000000019376",
        ...     # the Klout topic URL
        ...     "url": "http://klout.com/topic/id/10000000000000019376",
        ...     # the Klout topic name
        ...     "name": "Emoji"
        ... },
        ... {
        ... "score": 0.43,
        ... "id": "9159",
        ... "url": "http://klout.com/topic/id/9159",
        ... "name": "Vegetables"
        ... }]
    """
    try:
        # check that the dict paths exist
        if is_original_format(tweet):
            topics = tweet['user']['derived']['klout']['{}_topics'.format(topic_type)]
        else:
            topics = tweet['gnip']['klout_profile']['topics']
    except KeyError:
        return None
    # since we have topics, collect the right pieces
    topics_list = []
    if is_original_format(tweet):
        for topic in topics:
            # note: this is the same as the current structure of OF
            # payloads, but is written out for consistency w/ AS payloads
            this_topic = dict(url=topic['url'],
                              id=topic['id'],
                              name=topic['name'],
                              score=topic['score'])
            topics_list.append(this_topic)
    else:
        relevant_topics = [x for x in topics if x['topic_type'] == topic_type]
        for topic in relevant_topics:
            this_topic = dict(url=topic['link'],
                              id=topic['id'],
                              name=topic['displayName'],
                              score=topic['score'])
            topics_list.append(this_topic)
    sorted_topics_list = sorted(topics_list, key=lambda x: x['score'])
    return sorted_topics_list
