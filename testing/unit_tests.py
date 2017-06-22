import unittest
import gnip_tweet_parser as gtp
import fileinput
from create_test_cases import make_a_string
import json

class TestTweetMethods(unittest.TestCase):

    def setUp(self):
        tweet_payloads = {}
        tweet_payloads["activity_streams"] = {}
        tweet_payloads["original_format"] = {}
        tweet_ids = []
        for line in fileinput.FileInput("tweet_payload_examples/activity_streams_examples.json"):
            tweet = gtp.Tweet(json.loads(line))
            tweet_ids.append(tweet.id)
            tweet_payloads["activity_streams"][tweet.id] = tweet
        for line in fileinput.FileInput("tweet_payload_examples/original_format_examples.json"):
            tweet = gtp.Tweet(json.loads(line))
            tweet_ids.append(tweet.id)
            tweet_payloads["original_format"][tweet.id] = tweet
        self.tweet_payloads = tweet_payloads
        self.tweet_ids = list(set(tweet_ids))

        list_of_attrs = sorted([x for x in list(set(dir(gtp.Tweet)) - set(dir(dict))) if x[0] != "_"])
        self.list_of_attrs = list_of_attrs

    def test_equivalent_formats(self):
        for attr in self.list_of_attrs:
            for tweet_id in self.tweet_ids:
                # we know that we can't get polls in activity streams
                if self.tweet_payloads["original_format"][tweet_id].poll_options == []:
                    try:
                        orig = getattr(self.tweet_payloads["original_format"][tweet_id],attr)
                        if type(orig) == gtp.Tweet:
                            orig = orig.id
                    except gtp.NotAvailableError as e:
                        orig = e.__repr__()
                    try:
                        acti = getattr(self.tweet_payloads["activity_streams"][tweet_id],attr)
                        if type(acti) == gtp.Tweet:
                            acti = acti.id
                        acti = acti
                    except gtp.NotAvailableError as e:
                        acti = e.__repr__() 
                    # for some reason the ["body"]/["text"] truncations are different in as vs og
                    if attr == "text":
                        orig = orig[0:100]
                        acti = acti[0:100]
                    if attr != "poll_options": # the poll_options will raise an error an activity streams
                        self.assertEqual(orig,acti)

    def test_no_format_changes(self):
        for tweet_id in self.tweet_ids:
            for format in ["original_format","activity_streams"]:
                for attr in self.list_of_attrs:
                    # get the attribute of the tweets that we have loaded
                    try:
                        value = getattr(self.tweet_payloads[format][tweet_id],attr)
                        if type(value) != dict and type(value) != gtp.Tweet and type(value) != list:
                            value = make_a_string(value)
                    except gtp.NotATweetError as nate:
                        value = nate.__repr__()
                    except gtp.NotAvailableError as nae:
                        value = nae.__repr__()
                    # get the saved results from previously
                    try:
                        f = open("tweet_payload_examples/test_cases/{}/{}".format(attr,tweet_id+"_"+format), "r")
                        answer = f.read()
                        f.close()
                        if type(value) == dict or type(value) == list:
                            answer = json.loads(answer)
                        elif type(value) == gtp.Tweet:
                            answer = gtp.Tweet(json.loads(answer))
                    except FileNotFoundError:
                        raise FileNotFoundError(
                            "No test case created for this attibute/tweet: {}/{}".format(attr,tweet_id))
                    # check that the two are equal
                    self.assertEqual(answer,value)

if __name__ == '__main__':
    unittest.main()
