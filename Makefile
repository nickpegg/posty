.PHONY: doc

all: develop doc test

clean:
	rm -rf dist build
	rm -rf doc/_build

develop:
	pip install --upgrade pip uv
	uv sync --locked --dev

doc:
	(cd doc; make apidoc html man)

test:
	uv run black posty tests
	# Line length of 90 to work with Black formatting
	uv run flake8 --max-line-length=90 posty tests
	uv run mypy posty tests
	uv run pytest

test-watch:
	find . -name '*py' -or -name 'uv.lock' | entr -r -c make test

# Release-related actions
dist:
	uv build
	gpg --detach-sign -a dist/*tar.gz
	gpg --detach-sign -a dist/*whl

upload: dist
	uv publish --dry-run
