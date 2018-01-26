.PHONY: doc

all: develop doc test

clean:
	rm -rf dist build
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
	python setup.py sdist bdist_wheel
	gpg --detach-sign -a dist/*tar.gz
	gpg --detach-sign -a dist/*whl

upload:
	twine upload dist/*tar.gz dist/*whl dist/*asc
