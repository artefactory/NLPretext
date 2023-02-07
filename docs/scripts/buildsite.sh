#!/bin/bash

export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

##############
# BUILD DOCS #
##############

# Python Sphinx, configured with source/conf.py
# See https://www.sphinx-doc.org/

cd docs/

current_tag=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
current_tag_message=$(git cat-file -p $(git rev-parse $(git tag -l | tail -n1)) | tail -n +6)

make clean
make apidoc
git add .
git commit -m "Commit needed for multiversioning"

git pull --tags
git tag -a latest -m "Latest version of the package"

make multiversion

#######################
# Update GitHub Pages #
#######################

docroot=`mktemp -d`
cp -r build/html/* ${docroot}

cd ..

git branch -d gh-pages
git checkout --orphan gh-pages
git rm --cached -r .
git clean -fdx

# Adds .nojekyll file to the root to signal to GitHub that
# directories that start with an underscore (_) can remain
touch .nojekyll

# Add index.html
cat > index.html <<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>Redirecting to the latest release</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=./latest/index.html">
    <link rel="canonical" href="./latest/index.html">
  </head>
</html>
EOF

# Add README
cat > README.md <<EOF
# README for the GitHub Pages Branch
This branch is simply a cache for the website and is not intended to be viewed on github.com.
EOF

# Copy the resulting html pages built from Sphinx to the gh-pages branch
cp -r ${docroot}/* .

git add .

# Make a commit with changes and any new files
msg="Updating Docs for commit ${GITHUB_SHA} made on `date -d"@${SOURCE_DATE_EPOCH}" --iso-8601=seconds` from ${GITHUB_REF} by ${GITHUB_ACTOR}"
git commit -m "${msg}"

# overwrite the contents of the gh-pages branch on our github.com repo
git push origin gh-pages --force

# exit cleanly
exit 0
