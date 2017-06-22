from tweet_methods.tweet_parser_errors import InvalidJSONError, NotATweetError, NotAvailableError

def get_geo_coordinates(tweet):
    """ 
    return the geo coordinates, if they are included in the payload
    else raise 'unavailable field' error
    """
    if "geo" in tweet:
        if tweet["geo"] is not None:
            if "coordinates" in tweet["geo"]:
                [lat,lon] = tweet["geo"]["coordinates"]
                return {"latitude": lat, "longitude": lon}
    raise(NotAvailableError("Geo coordinates are not included in this Tweet"))