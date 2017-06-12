from setuptools import setup, find_packages

setup(name='gnip-tweet-parser',
        packages=find_packages(),
        scripts=["gnip_tweet_parser.py"],
        version='1.0.0.dev1',
        license='MIT',
        author='Fiona Pigott',
        author_email='fpigott@twitter.com',
        description="Tools for Tweet parsing", 
        url='https://github.com/fionapigott/tweet-parser',
        install_requires=[]
        )
