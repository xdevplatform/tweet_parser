#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Error: Please provide a branch name from which documentation will be built";
  exit 1
fi

BRANCH_NAME=$1

echo "Building documentation from $BRANCH_NAME"
echo "checking out gh-pages"
if ! git checkout gh-pages
then
  echo >&2 "checkout of gh-pages branch failed; please ensure you have local changes commited prior to running this script "
  echo "exiting"
  exit 1
fi

pwd
echo "removing current files"
rm -rf *.egg-info
git pull origin gh-pages
rm -r *.html *.js
touch .nojekyll
git checkout $BRANCH_NAME docs tweet_parser README.rst
# need to do this step because the readme will be overwritten
# pandoc -i README.md -o docs/source/README.rst
mv docs/* .
make html
mv -fv build/html/* ./
rm -r tweet_parser docs build Makefile source __pycache__/
echo "--------------------------------------------------------------------"
echo " docs built; please review these changes and then run the following:"
echo "--------------------------------------------------------------------"
echo git add -A
echo git commit -m \"Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit | grep commit`\"
echo git push origin gh-pages
echo git checkout $BRANCH_NAME
