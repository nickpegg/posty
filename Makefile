.PHONY: doc

all: develop doc test

clean:
	rm -rf dist build
	rm -rf doc/_build

develop:
	which pyenv >/dev/null && pyenv install -s
	pip install --upgrade pip poetry
	poetry install

doc:
	(cd doc; make apidoc html man)

test:
	poetry run pycodestyle posty tests
	poetry run flake8 posty tests
	poetry run pytest

# Release-related actions
dist:
	poetry build
	gpg --detach-sign -a dist/*tar.gz
	gpg --detach-sign -a dist/*whl

upload: dist
	poetry publish --dry-run
