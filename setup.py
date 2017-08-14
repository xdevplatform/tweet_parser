from setuptools import setup, find_packages

setup(name='tweet_parser',
      packages=find_packages(),
      scripts=["tools/parse_tweets.py"],
      version='1.0.5',
      license='MIT',
      author='Fiona Pigott',
      author_email='fpigott@twitter.com',
      description="Tools for Tweet parsing",
      url='https://github.com/tw-ddis/tweet_parser',
      install_requires=[],
      package_data={
          'tweet_parser': ['test/tweet_payload_examples/activity_streams_examples.json',
                           'test/tweet_payload_examples/original_format_examples.json',
                           'test/tweet_payload_examples/broken_and_unsupported_payloads/*.json'],
          },
      )
