## Documentation
We are using Sphinx with Google-style docstrings to build our documentation. It's a fairly straightforward process to build the docs locally to preview your changes. There is a script for deployment to gh-pages, described below.

### Setup

We obviously require sphinx for this, but (shinx_bootstrap)[https://github.com/ryan-roemer/sphinx-bootstrap-theme] is required for building the docs in Bootstrap.

on osx:

```.bash
pip install sphinx
pip install recommonmark
pip install spinx-bootstrap-theme
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
