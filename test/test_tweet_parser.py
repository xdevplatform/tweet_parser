import unittest
import fileinput
import json
from tweet_parser.tweet import Tweet
from tweet_parser import tweet_checking
from tweet_parser.tweet_parser_errors import NotATweetError, NotAvailableError, UnexpectedFormatError


def make_a_string(data):
    if type(data) == str:
        return data
    elif type(data) == set:
        return "{" + ", ".join(sorted(list(data))) + "}"
    else:
        return data.__repr__()


class TestTweetMethods(unittest.TestCase):

    def setUp(self):
        tweet_payloads = {}
        tweet_payloads["activity_streams"] = {}
        tweet_payloads["original_format"] = {}
        tweet_ids = []
        for line in fileinput.FileInput("tweet_payload_examples/activity_streams_examples.json"):
            tweet = Tweet(json.loads(line))
            tweet_ids.append(tweet.id)
            tweet_payloads["activity_streams"][tweet.id] = tweet
        for line in fileinput.FileInput("tweet_payload_examples/original_format_examples.json"):
            tweet = Tweet(json.loads(line))
            tweet_ids.append(tweet.id)
            tweet_payloads["original_format"][tweet.id] = tweet
        self.tweet_payloads = tweet_payloads
        self.tweet_ids = list(set(tweet_ids))

    def test_equivalent_formats(self):
        list_of_attrs = sorted([x for x in list(set(dir(Tweet)) - set(dir(dict))) if x[0] != "_"])
        for tweet_id in self.tweet_ids:
            # we know that we can't get polls in activity streams
            if self.tweet_payloads["original_format"][tweet_id].poll_options == []:
                for attr in list_of_attrs:
                    try:
                        orig = getattr(self.tweet_payloads["original_format"][tweet_id], attr)
                        if type(orig) == Tweet:
                            orig = orig.id
                    except NotAvailableError as e:
                        orig = e.__repr__()
                    try:
                        acti = getattr(self.tweet_payloads["activity_streams"][tweet_id], attr)
                        if type(acti) == Tweet:
                            acti = acti.id
                        acti = acti
                    except NotAvailableError as e:
                        acti = e.__repr__()
                    # for some reason the ["body"]/["text"] truncations are different in as vs og
                    if attr == "text":
                        orig = orig[0:100]
                        acti = acti[0:100]
                    if attr != "poll_options":  # the poll_options will raise an error in activity streams
                        self.assertEqual(orig, acti)

    def test_bad_payloads(self):
        # missing the user field, raises a "NotATweetError"
        with self.assertRaises(NotATweetError):
            f = open("tweet_payload_examples/broken_and_unsupported_payloads/original_format_missing_user.json", "r")
            tweet = json.load(f)
            f.close()
            Tweet(tweet)
        # missing a different required field, raises "UnexpectedFormatError"
        with self.assertRaises(UnexpectedFormatError):
            f = open("tweet_payload_examples/broken_and_unsupported_payloads/original_format_missing_field.json", "r")
            tweet = json.load(f)
            f.close()
            Tweet(tweet, do_format_checking=True)
        # missing a different required field, raises "UnexpectedFormatError"
        with self.assertRaises(UnexpectedFormatError):
            f = open("tweet_payload_examples/broken_and_unsupported_payloads/activity_streams_missing_field.json", "r")
            tweet = json.load(f)
            f.close()
            Tweet(tweet, do_format_checking=True)
        # added a new field, raises "UnexpectedFormatError"
        with self.assertRaises(UnexpectedFormatError):
            f = open("tweet_payload_examples/broken_and_unsupported_payloads/activity_streams_additional_field.json", "r")
            tweet = json.load(f)
            f.close()
            Tweet(tweet, do_format_checking=True)
        # added a new field, raises "UnexpectedFormatError"
        with self.assertRaises(UnexpectedFormatError):
            f = open("tweet_payload_examples/broken_and_unsupported_payloads/original_format_additional_field.json", "r")
            tweet = json.load(f)
            f.close()
            Tweet(tweet, do_format_checking=True)
        # note: these tests aren't going to cover some kinds of malformed payloads (i.e., "quote tweet" section is missing fields)

    def test_check_format(self):
        superset = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        minset = {2, 4, 6, 8, 10}
        too_many_keys = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        too_few_keys = {2, 4, 6, 8}
        just_right = {1, 2, 4, 6, 8, 10}
        with self.assertRaises(UnexpectedFormatError) as exception:
            tweet_checking.check_format(too_many_keys, superset, minset)
        with self.assertRaises(UnexpectedFormatError) as exception:
            tweet_checking.check_format(too_few_keys, superset, minset)
        self.assertEqual(0, tweet_checking.check_format(just_right, superset, minset))

    def test_get_all_keys(self):
        # define a test nested dict:
        test_dict = {"a": {"b": "c", "d": {"e": "f", "g": "h"}}, "i": "j"}
        self.assertEqual(set(tweet_checking.get_all_keys(test_dict)), {"a b", "a d e", "a d g", "i"})


if __name__ == '__main__':
    unittest.main()
