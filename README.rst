Tweet Parser
============

Authors: `Fiona Pigott <https://github.com/fionapigott>`__, `Jeff
Kolb <https://github.com/jeffakolb>`__, `Josh
Montague <https://github.com/jrmontag>`__, `Aaron
Gonzales <https://github.com/binaryaaron>`__

Goal:
-----

Allow reliable parsing of Tweets delivered by the Gnip platform, in both
activity-streams and original formats.

Status:
-------

This package can be installed by cloning the repo and using
``pip install -e .``, or by using ``pip install tweet_parser``. First
probably-bug-free release is 1.0.3. As of version 1.0.5, the package
works with Python 2 and 3, and the API should be relatively stable.
Recommended to use the more recent release. Current release (As of
9/20/2017) is 1.0.9.

Currently, this parser does not explicitly support Public API Twitter
data.

Usage:
------

This package is intended to be used as a Python module inside your other
Tweet-related code. An example Python program (after pip installing the
package) would be:

::

    from tweet_parser.tweet import Tweet
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

I've also added simple command-line utility:

::

    python tools/parse_tweets.py -f"gnip_tweet_data.json" -c"created_at_string,all_text"

Testing:
--------

A Python ``test_tweet_parser.py`` package exists in ``test/``.

The most important thing that it tests is the equivalence of outputs
when comparing both activity-streams input and original-format input.
Any new getter will be tested by running
``test$ python test_tweet_parser.py``, as the test checks every method
attached to the Tweet object, for every test tweet stored in
``test/tweet_payload_examples``. For any cases where it is expected that
the outputs are different (e.g., outputs that depend on poll options),
conditional statements should be added to this test.

An option also exists for run-time checking of Tweet payload formats.
This compares the set of all Tweet field keys to a superset of all
possible keys, as well as a minimum set of all required keys, to make
sure that each newly loaded Tweet fits those parameters. This shouldn't
be run every time you load Tweets (for one, it's slow), but is
implemented to use as a periodic check against Tweet format changes.
This option is enabled with ``--do_format_validation`` on the command
line, and by setting the keyword argument ``do_format_validation`` to
``True`` when initializing a ``Tweet`` object.

Contributing
------------

Submit bug reports or feature requests through GitHub Issues, with
self-contained minimum working examples where appropriate.

To contribute code, fork this repo, create your own local feature
branch, make your changes, test them, and submit a pull request to the
master branch. The contribution guidelines specified in the ``pandas``
`documentation <http://pandas.pydata.org/pandas-docs/stable/contributing.html#working-with-the-code>`__
are a great reference.

When you submit a change, change the version number. For most minor,
non-breaking changes (fix a bug, add a getter, package naming/structure
remains the same), increment the last number (X.Y.Z -> X.Y.Z+1) in
``setup.py``.

Guidelines for new getters
~~~~~~~~~~~~~~~~~~~~~~~~~~

A *getter* is a method in the Tweet class and the accompanying code in
the ``getter_methods`` module. A getter for some property should:

- be named ``<property>``, a method in ``Tweet`` decorated with
  ``@lazy_property``
- have a corresponding method named
  ``get_<property>(tweet)`` in the ``getter_methods`` module that
  implements the logic, nested uner the appropriate submodule (a text
  property probably lives under the ``getter_methods.tweet_text``
  submodule) 
- provide the exact same output for original format and
  activity-streams format Tweet input, except in the case where certain
  information is unavailable (see ``get_poll_options``).

In general, prefer that the ``get_<property>`` work on a simple Tweet
dictionary as well as a Tweet object (this makes unit testing easier).
This means that you might use ``is_original_format(tweet)`` rather than
``tweet.is_original_format`` to check format inside of a getter.

Adding unit tests for your getter in the docstrings in the "Example"
section is helpful. See existing getters for examples.

In general, make detailed docstrings with examples in
``get_<property>``, and more concise dosctrings in ``Tweet``, with a
reference for where to find the ``get_<property>`` getter that
implements the logic.

Style
~~~~~

Adhere to the PEP8 style. Using a Python linter (like flake8) is
reccomended.

For documentation style, use `Google-style
docstrings <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`__.
Refer to the `Python docstest
documentation <https://docs.python.org/3/library/doctest.html>`__ for
doctest guidelines.

Testing
~~~~~~~

Create an isolated virtual environment for testing (there are currently
no external dependencies for this library).

Test your new feature by reinstalling the library in your virtual
environment and running the test script as shown below. Fix any issues
until all tests pass.

::

    (env) [tweet_parser]$ pip install -e .
    (env) [tweet_parser]$ cd test/; python test_tweet_parser.py; cd -

Furthermore, if contributing a new accessor or getter method for payload
elements, verify the code works as you intended by running the
``parse_tweets.py`` script with your new field, as shown below. Check
that both input types produce the intended output.

::

    (env) [tweet_parser]$ pip install -e .
    (env) [tweet_parser]$ python tools/parse_tweets.py -f test/tweet_payload_examples/activity_streams_examples.json -c <your new field>

And lastly, if you've added new docstrings and doctests, from the
``docs`` directory, run ``make html`` (to check docstring formatting)
and ``make doctest`` to run the doctests.
