from tweet_parser.tweet_checking import is_original_format


def get_user_id(tweet):
    """
    get the user id, as a string
    """
    if is_original_format(tweet):
        return tweet["user"]["id_str"]
    else:
        return tweet["actor"]["id"].split(":")[-1]


def get_screen_name(tweet):
    """
    get the user screen name (@ handle)
    """
    if is_original_format(tweet):
        return tweet["user"]["screen_name"]
    else:
        return tweet["actor"]["preferredUsername"]


def get_name(tweet):
    """
    get the user's display name
    """
    if is_original_format(tweet):
        return tweet["user"]["name"]
    else:
        return tweet["actor"]["displayName"]


def get_klout_score(tweet):
    """ 
    Return the user's Klout score (an int), if it exists.
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
    Return the user's Klout profile URL (an str), if it exists.
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
    Return the user's Klout id (an str), if it exists.
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
    Return the user's chosen Klout topics (a list of dicts), if it exists.

    Regardless of the format or topic type, the topic dicts will have the same keys:
        url, id, name, score 
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
            #  payloads, but is written out for consistency w/ AS payloads
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
    return topics_list 

