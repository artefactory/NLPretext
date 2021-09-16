# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS           ?=
SPHINXBUILD          ?= poetry run sphinx-build
SPHINXAPIBUILD       ?= poetry run sphinx-apidoc
SPHINXMULTIVERSION   ?= poetry run sphinx-multiversion
SOURCEDIR            = source
BUILDDIR             = build

# Put it first so that "make" without argument is like "make help".
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

multiversion:
	@$(SPHINXMULTIVERSION) $(SOURCEDIR) $(BUILDDIR)/html

apidoc:
	@$(SPHINXAPIBUILD) -f -o source/apidoc/ ../nlpretext/ --implicit-namespaces -M -t source/_templates

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
