PYTHON ?= python3
HUGO ?= hugo
RECIPES_DIR ?= recipes

.PHONY: build test
build:
	$(PYTHON) scripts/build.py --recipes "$(RECIPES_DIR)" --hugo "$(HUGO)"

test:
	$(PYTHON) -m unittest discover -s tests -v
