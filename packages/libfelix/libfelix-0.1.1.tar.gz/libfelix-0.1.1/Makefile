MAKEFLAGS += --always-make

default: ruff test

code-style: ruff mypy

ruff:
	ruff .

mypy:
	mypy .

test:
	pytest --doctest-modules

build:
	python -m build --no-isolation

clean:
	rm -rf build/ dist/

pre-release: clean code-style test build

release-test-pypi: pre-release
	twine upload --repository testpypi dist/*

release-pypi: pre-release
	twine upload --repository pypi dist/*
