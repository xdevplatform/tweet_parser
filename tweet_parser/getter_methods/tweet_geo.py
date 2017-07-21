from tweet_parser.tweet_checking import is_original_format


def get_geo_coordinates(tweet):
    """
    return the geo coordinates, if they are included in the payload
    else raise 'unavailable field' error
    """
    if "geo" in tweet:
        if tweet["geo"] is not None:
            if "coordinates" in tweet["geo"]:
                [lat, lon] = tweet["geo"]["coordinates"]
                return {"latitude": lat, "longitude": lon}
    return None


def get_profile_location(tweet):
    """
    return location data from the profile location profile location enrichment
    only provide the first element of the locations list (because idk what the other one means)
    return NotAvailableError if there is no field or the enrichment is not included in the tweet
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
