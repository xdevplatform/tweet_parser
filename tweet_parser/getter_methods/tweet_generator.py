# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from tweet_parser.tweet_checking import is_original_format
import sys
if sys.version_info[0] == 3:
    from html.parser import HTMLParser
elif sys.version_info[0] == 2:
    from HTMLParser import HTMLParser

class GeneratorHTMLParser(HTMLParser):
    """
    HTML parser class to handle HTML tags in the original format source field
    """
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                self.generator_link = attr[1]

    def handle_data(self, data):
        self.generator_name = data


def get_generator(tweet):
    """
    Get information about the application that generated the Tweet

    Args:
        tweet (Tweet): A Tweet object (or a dictionary)

    Returns:
        dict: keys are 'link' and 'name', the web link and the name
        of the application

    Example:
        >>> from tweet_parser.getter_methods.tweet_generator import get_generator
        >>> original_format_dict = {
        ...             "created_at": "Wed May 24 20:17:19 +0000 2017",
        ...             "source": '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>'
        ...            }
        >>> get_generator(original_format_dict)
        {'link': 'http://twitter.com', 'name': 'Twitter Web Client'}

        >>> activity_streams_format_dict = {
        ...             "postedTime": "2017-05-24T20:17:19.000Z",
        ...             "generator":
        ...              {"link": "http://twitter.com",
        ...               "displayName": "Twitter Web Client"}
        ...             }
        >>> get_generator(activity_streams_format_dict)
        {'link': 'http://twitter.com', 'name': 'Twitter Web Client'}
    """
    if is_original_format(tweet):
        if sys.version_info[0] == 3 and sys.version_info[1] >= 4:
            parser = GeneratorHTMLParser(convert_charrefs=True)
        else:
            parser = GeneratorHTMLParser()
        parser.feed(tweet["source"])
        return {"link": parser.generator_link,
                "name": parser.generator_name}
    else:
        return {"link": tweet["generator"]["link"],
                "name": tweet["generator"]["displayName"]}
