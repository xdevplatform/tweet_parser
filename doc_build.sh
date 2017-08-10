# Minimal makefile for Sphinx documentation
#
BRANCH_NAME=$1

if [ -z ${BRANCH_NAME+x} ] ;
  then echo "please provide a branch name from which documentation will be
    built";
  else echo "building docs from $BRANCH_NAME"
fi

echo "Building documentation"
echo "checking out gh-pages"
git checkout gh-pages
pwd
echo "removing current files"
rm -r *.html *.js docs/
touch .nojekyll
git checkout $BRANCH_NAME docs tweet_parser
mv docs/* .
make html
mv -fv build/html/* ./
rm -r tweet_parser docs build Makefile source
git add -A
git commit -m "Generated gh-pages for `git log $BRANCH_NAME -1 --pretty=short --abbrev-commit`"
# git push origin gh-pages
# git checkout $BRANCH_NAME
