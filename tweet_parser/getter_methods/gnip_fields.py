def get_matching_rules(tweet):
    """
    Retrieves the matching rules for a tweet with a gnip field enrichment.

    Args:
        tweet (Tweet): the tweet

    Returns:
        list of potential [{"tag": "rule"}] pairs from standard rulesets or
        None if no rules or no field gnip is found.

    """
    gnip = tweet.get("gnip")
    rules = gnip.get("matching_rules") if gnip else None
    return rules
