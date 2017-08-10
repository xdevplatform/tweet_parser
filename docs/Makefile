# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = TweetParser
SOURCEDIR     = source
BUILDDIR      = build
GH_PAGES_SOURCES = docs tweet_parser

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

gh-pages:
	echo "checking out gh-pages"
	git checkout gh-pages
	cd ..
	pwd
	echo "removing current files"
	# rm -rf .
	# git checkout doc_builder $(GH_PAGES_SOURCES)
	# ls -all
	# mv docs/* .
	# make html
	# mv -fv build/html/* ./
	# rm -rf $(GH_PAGES_SOURCES) build Makefile source


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

