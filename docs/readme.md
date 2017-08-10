## Documentation
We are using Sphinx with Google-style docstrings to build our documentation. It's a fairly straightforward process to build the docs locally to preview your changes. There is a script for deployment to gh-pages, described below.

### Setup

```.bash
pip install sphinx
pip install sphinx_bootstrap_theme
```

### Build

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
