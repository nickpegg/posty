.PHONY: doc

all: develop doc test

develop:
	pip install -r requirements.dev.txt

doc:
	(cd doc; make apidoc html man)

test:
	pycodestyle posty tests
	flake8 posty tests
	pytest
