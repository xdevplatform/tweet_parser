# gnip-tweet-parser
Authors: Fiona Pigott, Jeff Kolb

## Goal:
Allow reliable parsing of Tweets delivered by the Gnip platform, in both activity-streams and original formats. 

## Status:
This package is not yet available on pypi, but soon it should be. For now, recommended usage would be to clone the repository and `pip install -e .`

## Usage:
This package is intended to be used as a Python module inside your other Tweet-related code. An example Python program (after pip installing the package) would be:

```
import gnip_tweet_parser as gtp
import fileinput
import ujson

for line in fileinput.FileInput("gnip_tweet_data.json"):
    try:
        tweet_dict = ujson.loads(line)
        tweet = gtp.Tweet(tweet_dict)
    except (ValueError,gtp.NotATweetError):
        pass
    print(tweet.created_at_string, tweet.all_text)
```

I've also added simple command-line utility:

```
python gnip_tweet_parser.py -f"gnip_tweet_data.json" -c"created_at_string,all_text"
```
