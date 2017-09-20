from setuptools import setup, find_packages

setup(name='tweet_parser',
      description="Tools for Tweet parsing",
      url='https://github.com/tw-ddis/tweet_parser',
      author='Fiona Pigott, Jeff Kolb, Josh Montague, Aaron Gonzales',
      long_description=open('README.rst', 'r').read(),
      author_email='fpigott@twitter.com',
      license='MIT',
      version='1.0.9',
      packages=find_packages(),
      scripts=["tools/parse_tweets.py"],
      install_requires=[],
      )
