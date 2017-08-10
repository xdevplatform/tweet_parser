# Minimal makefile for Sphinx documentation
#
BRANCH_NAME=$1

if [ -z ${BRANCH_NAME+x} ] ;
  then echo "please provide a branch name from which documentation will be built";
  else echo "building docs from $BRANCH_NAME"
fi

echo "Building documentation"
echo "checking out gh-pages"
if ! git checkout gh-pages
then
  echo >&2 "checkout of gh-pages branch failed; please ensure you have local changes commited prior to running this script "
  echo "exiting"
  exit 1
fi

pwd
echo "removing current files"
rm -r *.html *.js docs/
touch .nojekyll
git checkout $BRANCH_NAME docs tweet_parser
mv docs/* .
make html
mv -fv build/html/* ./
rm -r tweet_parser docs build Makefile source
echo "please review these changes and then run the following:"
echo git add -A
echo git commit -m "Generated gh-pages for `git log $BRANCH_NAME -1 --pretty=short --abbrev-commit`"
echo git push origin gh-pages
echo git checkout $BRANCH_NAME
