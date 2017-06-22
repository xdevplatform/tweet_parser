import gnip_tweet_parser as gtp
import os
import fileinput
import json

def make_a_string(data):
    if type(data) == str:
        return data
    elif type(data) == set:
        return "{" + ",".join(sorted(list(data))) + "}"
    else:
        return data.__repr__()

# create on dir per attr
# create one file per Tweet
tweet_payloads = {}
for line in fileinput.FileInput("tweet_payload_examples/activity_streams_examples.json"):
    tweet = gtp.Tweet(json.loads(line))
    tweet_payloads[tweet.id + "_activity_streams"] = tweet
for line in fileinput.FileInput("tweet_payload_examples/original_format_examples.json"):
    tweet = gtp.Tweet(json.loads(line))
    tweet_payloads[tweet.id + "_original_format"] = tweet


list_of_attrs = sorted([x for x in list(set(dir(gtp.Tweet)) - set(dir(dict))) if x[0] != "_"])
for attr in list_of_attrs:
    attr_dir = "tweet_payload_examples/test_cases/{}".format(attr)
    if not os.path.exists(attr_dir):
        os.makedirs(attr_dir)
    for id_key in tweet_payloads:
        if not os.path.isfile(attr_dir + "/{}".format(id_key)):
            print("Creating data to test the {} attribute of {}".format(attr,id_key))
            f = open(attr_dir + "/{}".format(id_key), "w")
            try:
                value = getattr(tweet_payloads[id_key],attr)
                if type(value) == dict or type(value) == gtp.Tweet or type(value) == list:
                    value = json.dumps(value)
                else:
                    value = make_a_string(value)
            except gtp.NotATweetError as nate:
                value = nate.__repr__()
            except gtp.NotAvailableError as nae:
                value = nae.__repr__()
            f.write(value)
            f.close()
            print(value)



