def get_geo_coordinates(tweet_dict, is_original_format):
    """ 
    return the geo coordinates, if they are included in the payload
    else raise 'unavailable field' error
    """
    if "geo" in tweet_dict:
        if tweet_dict["geo"] is not None:
            if "coordinates" in tweet_dict["geo"]:
                [lat,lon] = tweet_dict["geo"]["coordinates"]
                return {"latitude": lat, "longitude": lon}
    raise(NotAvailableError("Geo coordinates are not included in this Tweet"))