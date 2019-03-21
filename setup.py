# -*- coding: utf-8 -*-
# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
from setuptools import setup, find_packages

setup(name='tweet_parser',
      description="Tools for Tweet parsing",
      url='https://github.com/twitterdev/tweet_parser',
      author='Fiona Pigott, Jeff Kolb, Josh Montague, Aaron Gonzales',
      long_description=open('README.rst', 'r').read(),
      author_email='fpigott@twitter.com',
      license='MIT',
      version='1.13.2',
      packages=find_packages(),
      scripts=["tools/parse_tweets.py"],
      install_requires=[],
     )
