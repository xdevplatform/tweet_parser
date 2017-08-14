from tweet_parser.tweet_checking import is_original_format


def get_geo_coordinates(tweet):
    """
    Get the user's geo coordinates, if they are included in the payload
    (otherwise return None)

    Args:
        tweet (Tweet or dict): A Tweet object or dictionary

    Returns:
        dict: dictionary with the keys "latitude" and "longitude"
              or, if unavaiable, None

    Example:
        >>> from tweet_parser.getter_methods.tweet_geo import get_geo_coordinates
        >>> tweet_geo = {"geo": {"coordinates": [1,-1]}}
        >>> get_geo_coordinates(tweet_geo)
        {'latitude': 1, 'longitude': -1}

        >>> tweet_no_geo = {"geo": {}}
        >>> get_geo_coordinates(tweet_no_geo) #returns None
    """
    if "geo" in tweet:
        if tweet["geo"] is not None:
            if "coordinates" in tweet["geo"]:
                [lat, lon] = tweet["geo"]["coordinates"]
                return {"latitude": lat, "longitude": lon}
    return None


def get_profile_location(tweet):
    """
    Get user's derived location data from the profile location enrichment
    If unavailable, returns None.

    Args:
        tweet (Tweet or dict): Tweet object or dictionary

    Returns:
        dict: more information on the profile locations enrichment here:
        http://support.gnip.com/enrichments/profile_geo.html

    Example:
        >>> result = {"country": "US",         # Two letter ISO-3166 country code
        ...           "locality": "Boulder",   # The locality location (~ city)
        ...           "region": "Colorado",    # The region location (~ state/province)
        ...           "sub_region": "Boulder", # The sub-region location (~ county)
        ...           "full_name": "Boulder, Colorado, US", # The full name (excluding sub-region)
        ...           "geo":  [40,-105]        # lat/long value that coordinate that corresponds to
        ...                            # the lowest granularity location for where the user
        ...                            # who created the Tweet is from
        ...  }

    Caveats:
        This only returns the first element of the 'locations' list.
        I'm honestly not sure what circumstances would result in a list that
        is more than one element long.
    """
    if is_original_format(tweet):
        try:
            return tweet["user"]["derived"]["locations"][0]
        except KeyError:
            return None
    else:
        try:
            location = tweet["gnip"]["profileLocations"][0]
            reconstructed_original_format = {}
            if location["address"].get("country", None) is not None:
                reconstructed_original_format["country"] = location["address"]["country"]
            if location["address"].get("countryCode", None) is not None:
                reconstructed_original_format["country_code"] = location["address"]["countryCode"]
            if location["address"].get("locality", None) is not None:
                reconstructed_original_format["locality"] = location["address"]["locality"]
            if location["address"].get("region", None) is not None:
                reconstructed_original_format["region"] = location["address"]["region"]
            if location["address"].get("subRegion", None) is not None:
                reconstructed_original_format["sub_region"] = location["address"]["subRegion"]
            if location.get("displayName", None) is not None:
                reconstructed_original_format["full_name"] = location["displayName"]
            if location.get("geo", None) is not None:
                reconstructed_original_format["geo"] = location["geo"]
            return reconstructed_original_format
        except KeyError:
            return None
