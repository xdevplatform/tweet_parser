from setuptools import setup, find_packages

setup(name='gnip-tweet-parser',
      packages=find_packages(),
      scripts=["gnip_tweet_parser/gnip_tweet_parser.py"],
      version='1.0.0.dev1',
      license='MIT',
      author='Fiona Pigott',
      author_email='fpigott@twitter.com',
      description="Tools for Tweet parsing",
      url='https://github.com/fionapigott/tweet-parser',
      install_requires=[],
      python_requires='>=3',
      package_data={
          'gnip-tweet-parser': ['test/tweet_payload_examples/activity_streams_examples.json',
                                'test/tweet_payload_examples/original_format_examples.json',
                                'test/tweet_payload_examples/broken_and_unsupported_payloads/*.json'],
          },
      )
