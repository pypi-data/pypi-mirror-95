# Hycli

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hycli)](https://pypi.org/project/hycli/)
[![PyPI version](https://badge.fury.io/py/hycli.svg)](https://pypi.org/project/hycli/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Main workflow](https://github.com/hypatos/hycli/workflows/Main%20workflow/badge.svg)

This repository contains a Python package/CLI tool to batch extract documents through the Hypatos API and to compare the results.

## Quickstart

```
pip install hycli
hycli extract path-to-files [to-xlsx|to-csv|to-json] url
hycli compare workbook1 workbook2
```

For more information without leaving the cli use ```hycli --help```

## API Reference and User Guide [available](https://hypatos.github.io/hycli/)

---

## Development

### Requirement

- [poetry](https://python-poetry.org/)

### Installing

```
poetry install
poetry shell
hycli --help
```

### Running the tests

```
poetry run pytest
```

### Versioning

Uses [bump2version](https://github.com/c4urself/bump2version):

```
bump2version --verbose [patch|minor|major]  # add --dry-run to have a preview
git push --follow-tags
```

### Documentation

Is build with sphinx, can be seen/worked on locally by:

```
cd docs
make html
open build/html/index.html
```

### License

Hypatos
