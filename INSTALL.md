# Installation Guide

## From PyPI (Recommended)

```bash
pip install ilovepdf
```

## From Source

Install the latest version directly from GitHub:

```bash
pip install -U git+https://github.com/ilovepdf/ilovepdf-python.git@main#egg=ilovepdf
```

## Pre-release Versions

Test upcoming versions from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ilovepdf
```

> **Note:** The `--extra-index-url` flag is required because TestPyPI doesn't host all dependency versions.

## Requirements

- Python 3.10 - 3.14
- Dependencies: `requests>=2.28.0`, `pyjwt>=2.4.0`, `python-dotenv>=1.0.0`

## Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install ilovepdf
```
