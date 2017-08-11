# tweet_parser 
Authors: Fiona Pigott, Jeff Kolb, Josh Montague, Aaron Gonzales

## Goal: 
Allow reliable parsing of Tweets delivered by the Gnip platform, in both
activity-streams and original formats. 

## Status: 
This package can be installed by cloning the repo and using `pip install -e .`,
or by using `pip install tweet_parser`. First probably-bug-free release is
1.0.3 (current as of 8/7/2017). No promises.

Currently, this parser does not explicitly support Public API Twitter data.

## Usage: 
This package is intended to be used as a Python module inside your other
Tweet-related code. An example Python program (after pip installing the
package) would be:

```
from tweeet_parser.tweet import Tweet
from tweet_parser.tweet_parser_errors import NotATweetError
import fileinput
import json

for line in fileinput.FileInput("gnip_tweet_data.json"):
    try:
        tweet_dict = json.loads(line)
        tweet = Tweet(tweet_dict)
    except (json.JSONDecodeError,NotATweetError):
        pass
    print(tweet.created_at_string, tweet.all_text)
```

I've also added simple command-line utility:

```
python tools/parse_tweets.py -f"gnip_tweet_data.json" -c"created_at_string,all_text"
```

## Testing: 
A Python `test_tweet_parser.py` package exists in `test/`. 

The most important thing that it tests is the equivalence of outputs when
comparing both activity-streams input and original-format input. Any new getter
will be tested by running `test$ python test_tweet_parser.py`, as the test
checks every method attached to the Tweet object, for every test tweet stored
in `test/tweet_payload_examples`. For any cases where it is expected that the
outputs are different (e.g., outputs that depend on poll options), conditional
statements should be added to this test.

An option also exists for run-time checking of Tweet payload formats. This
compares the set of all Tweet field keys to a superset of all possible keys, as
well as a minimum set of all required keys, to make sure that each newly loaded
Tweet fits those parameters. This shouldn't be run every time you load Tweets
(for one, it's slow), but is implemented to use as a periodic check against
Tweet format changes. This option is enabled with `--do_format_checking` on the
command line, and by setting the keyword argument `do_format_checking` to
`True` when initializing a `Tweet` object.

## Documentation
We are using Sphinx with Google-style docstrings to build our documentation. If
you don't have sphinx installed, it's a quick `pip install sphinx`. 
To build the docs locally, follow:

### Setup

```
pip install sphinx
pip install sphinx_bootstrap_theme
```

### Build

```
cd tweet_parser/docs
make clean
make html
```

### Deploying to github pages
From the root of the repo run:

```
bash doc_build.sh <BRANCH_NAME>
```

where `<BRANCH_NAME>` is the name of the branch you'll be building from, most likely master. The script will change to the `gh-pages` branch, clean out the olds docs, pull your changes from the relevant branch, build them, and give you instructions for review and commands for deployment.


## Contributing

Submit bug reports or feature requests through GitHub Issues, with
self-contained minimum working examples where appropriate.   

To contribute code, the guidelines specified in the [`pandas`
documentation](http://pandas.pydata.org/pandas-docs/stable/contributing.html#working-with-the-code)
are a great reference. Fork this repo, create your own local feature branch,
and create an isolated virtual environment (there are currently no external
dependencies for this library). Using a Python linter is recommened. 

Test your new feature by reinstalling the library in your virtual environment
and running the test script as shown below. Fix any issues until all tests
pass. 

```
(env) [tweet_parser]$ pip install -e .
(env) [tweet_parser]$ cd test/; python test_tweet_parser.py; cd -
```

Furthermore, if contributing a new accessor or getter method for payload
elements, verify the code works as you intended by running the
`parse_tweets.py` script with your new field, as shown below. Check that both
input types produce the intended output. 

```
(env) [tweet_parser]$ pip install -e .
(env) [tweet_parser]$ python tools/parse_tweets.py -f test/tweet_payload_examples/activity_streams_examples.json -c <your new field>
```

Change the version number. For most minor, non-breaking changes (fix a bug, add
a getter, package naming/structure remains the same), simply update the last
number (Z of X.Y.Z) in `setup.py`.
