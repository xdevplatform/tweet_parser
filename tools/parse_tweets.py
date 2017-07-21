#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tweet_parser.tweet import Tweet
from tweet_parser.tweet_parser_errors import NotATweetError, NotAvailableError
import argparse
import fileinput
import sys
try:
    import ujson as json
    JSONDecodeError = ValueError
except ImportError:
    import json
    JSONDecodeError = json.JSONDecodeError

parser = argparse.ArgumentParser(
    description="Parse seqeunce of JSON formated activities.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--file", dest="data_files",
                    default="-",
                    help="Name of the file to read from, defaults to stdin")
list_of_attrs = sorted([x for x in list(set(dir(Tweet)) - set(dir(dict))) if x[0] != "_"])
parser.add_argument("-c", "--csv", dest="func_list",
                    default="id",
                    help="comma separated list of attibutes to get \n possible functions include: \n -> {}".format(" \n -> ".join(list_of_attrs)))
parser.add_argument("-d", "--delim", dest="delim",
                    default="|",
                    help="delimiter for the output csv, defaults to pipe")
parser.add_argument("-z", "--compressed", action="store_true", dest="compressed",
                    default=False,
                    help="use this flag if data is compressed")
parser.add_argument("-j", "--pass_bad_json", action="store_true", dest="pass_bad_json",
                    default=False,
                    help="use this flag to silently pass bad JSON payloads")
parser.add_argument("-t", "--pass_non_tweet", action="store_true", dest="pass_non_tweet",
                    default=False,
                    help="use this flag to silently pass on non-tweet payloads")
parser.add_argument("-a", "--pass_not_available", action="store_true", dest="pass_not_available",
                    default=False,
                    help="use this flag to silently pass on non-tweet payloads")
parser.add_argument("--do_format_checking", action="store_true", dest="do_format_checking",
                    default=False,
                    help="debug formatting")
options = parser.parse_args()

# get the functions that we need to use:
functions = options.func_list.split(",")

# get the compression
if options.compressed:
    openhook = fileinput.hook_compressed
else:
    openhook = None
# parse some tweets
for line in fileinput.FileInput(options.data_files, openhook=openhook):
    csv = []
    # load the JSON
    try:
        tweet_dict = json.loads(line)
    except JSONDecodeError as json_error:
        if not options.pass_bad_json:
            sys.stderr.write("{}. Use the flag '-j' to pass silently next time.\nBad JSON payload: {}".format(json_error, line))
        continue
    # load a Tweet
    try:
        tweet_obj = Tweet(tweet_dict, do_format_checking=options.do_format_checking)
    except NotATweetError as nate:
        if not options.pass_non_tweet:
            sys.stderr.write("{}. Use the flag '-t' to pass silently next time.\nNon Tweet payload: {}".format(nate, line))
        continue
    # get the relevant fields
    for func in functions:
        try:
            attribute = getattr(tweet_obj, func)
            if type(attribute) == str:
                attribute = attribute.replace(options.delim, " ").replace("\n", " ").replace("\r", " ")
            csv.append(str(attribute))
        except NotAvailableError as nae:
            if not options.pass_not_available:
                sys.stderr.write("{}. Use the flag -a to pass silently next time.\nAttribute Unavailable: {}".format(nae, line))
            csv.append("NOT_AVAILABLE")
    sys.stdout.write(options.delim.join(csv) + "\n")
