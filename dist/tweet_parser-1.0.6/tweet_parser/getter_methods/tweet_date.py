# Twitter Snowflake ID to timestamp (and back)
# https://github.com/client9/snowflake2time/
# Nick Galbreath @ngalbreath nickg@client9.com
# Public Domain -- No Copyright -- Cut-n-Paste


def snowflake2utc(sf):
    """
    Convert a Twitter snowflake ID to a Unix timestamp
    (seconds since Jan 1 1970 00:00:00)

    Args:
        sf (str): Twitter snowflake ID as a string

    Returns:
        int: seconds since Jan 1 1970 00:00:00
    """
    sf_int = int(sf)
    return int(((sf_int >> 22) + 1288834974657) / 1000.0)
