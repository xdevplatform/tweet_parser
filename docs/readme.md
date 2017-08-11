## Documentation
We are using Sphinx with Google-style docstrings to build our documentation. It's a fairly straightforward process to build the docs locally to preview your changes. There is a script for deployment to gh-pages, described below.

### Setup

We obviously require sphinx for this, but (Pandoc)[https://pandoc.org/] is a requirement for the conversion script - it changes the base project readme file (tweet_parser/README.md) to a sphinx-compatible Restructured Text file.

on osx:

```.bash
brew install pandoc
pip install sphinx
pip install recommonmark
```

### Build

This will build the docs locally for testing and future deployment.

```.bash
cd tweet_parser/docs
make clean
make html
```

### Deploying to github pages
From the root of the repo run:

```.bash
bash doc_build.sh <BRANCH_NAME>
```

where `<BRANCH_NAME>` is the name of the branch you'll be building from, most likely master. The script will change to the `gh-pages` branch, clean out the olds docs, pull your changes from the relevant branch, build them, and give you instructions for review and commands for deployment.
