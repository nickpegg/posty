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
	uv run pycodestyle posty tests
	uv run flake8 posty tests
	uv run mypy posty tests
	uv run pytest

# Release-related actions
dist:
	uv build
	gpg --detach-sign -a dist/*tar.gz
	gpg --detach-sign -a dist/*whl

upload: dist
	uv publish --dry-run
