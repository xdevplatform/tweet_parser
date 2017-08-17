from tweet_parser.tweet_checking import is_original_format


def get_matching_rules(tweet):
    """
    Retrieves the matching rules for a tweet with a gnip field enrichment.

    Args:
        tweet (Tweet): the tweet

    Returns:
        list: potential ``[{"tag": "user_tag", "value": "rule_value"}]`` 
        pairs from standard rulesets or None if no rules or no
        matching_rules field is found. \n
        More information on this value at:
        http://support.gnip.com/enrichments/matching_rules.html

    """
    if is_original_format(tweet):
        rules = tweet.get("matching_rules")
    else:
        gnip = tweet.get("gnip")
        rules = gnip.get("matching_rules") if gnip else None
    return rules
