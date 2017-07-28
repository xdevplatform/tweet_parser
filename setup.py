from setuptools import setup, find_packages

setup(name='tweet_parser',
      packages=find_packages(),
      scripts=["tools/parse_tweets.py"],
      version='1.0.2.dev1',
      license='MIT',
      author='Fiona Pigott',
      author_email='fpigott@twitter.com',
      description="Tools for Tweet parsing",
      url='https://github.com/fionapigott/tweet_parser',
      install_requires=[],
      python_requires='>=3',
      package_data={
          'tweet_parser': ['test/tweet_payload_examples/activity_streams_examples.json',
                           'test/tweet_payload_examples/original_format_examples.json',
                           'test/tweet_payload_examples/broken_and_unsupported_payloads/*.json'],
          },
      )
