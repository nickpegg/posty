.PHONY: doc

all: develop doc test

develop:
	pip install -r requirements.dev.txt
	pip install -e .

doc:
	(cd doc; make doc)

test:
	pycodestyle posty tests
	flake8 posty tests
	pytest
