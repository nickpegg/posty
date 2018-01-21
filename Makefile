.PHONY: doc

all: develop doc test

clean:
	rm -rf dist
	rm -rf doc/_build

develop:
	pip install -r requirements.dev.txt

doc:
	(cd doc; make apidoc html man)

test:
	pycodestyle posty tests
	flake8 posty tests
	pytest

# Release-related actions
dist:
	python setup.py sdist
	gpg --detach-sign -a dist/*tar.gz

upload:
	twine upload dist/*tar.gz dist/*asc
