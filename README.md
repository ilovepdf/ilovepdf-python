# iLovePDF API - Python Library

[![PyPI version](https://img.shields.io/pypi/v/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)
[![Python versions](https://img.shields.io/pypi/pyversions/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)
[![License](https://img.shields.io/pypi/l/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)

A Python library for [iLovePDF API](https://developer.ilovepdf.com) to automate PDF processing tasks such as compressing, merging, splitting, converting, protecting, and more.

You can sign up for an iLovePDF account at https://developer.ilovepdf.com

Develop and automate PDF processing tasks like Compress PDF, Merge PDF, Split PDF, convert Office to PDF, PDF to JPG, Images to PDF, add Page Numbers, Rotate PDF, Unlock PDF, stamp a Watermark and Repair PDF. Each one with several settings to get your desired results.

---

## Requirements

- Python 3.10 to 3.14

---

> **Note:**  
> This library is fully compatible with Python versions 3.10, 3.11, 3.12, 3.13, and 3.14.  
> All features, tests, and Docker environments are validated for this range.  
> If you encounter any issues with a supported version, please report them via [GitHub Issues](https://github.com/ilovepdf/ilovepdf-python/issues).

---

## Installation

Install from PyPI:

```bash
pip install ilovepdf
```

Or install the latest version from source:

```bash
pip install -U git+https://github.com/ilovepdf/ilovepdf-python.git@main#egg=ilovepdf
```

### Install Pre-release Versions

To test pre-release versions from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ilovepdf
```

**Note:** The `--extra-index-url` flag is required because TestPyPI doesn't host all dependency versions.

---

## Getting Started

Simple usage looks like:

```python
from ilovepdf import CompressTask

task = CompressTask(public_key="your_public_key", secret_key="your_secret_key")
task.add_file("input.pdf")
task.execute()
task.download("output_folder")
```

---

## Project Structure & Documentation

- Core library: [`ilovepdf/`](ilovepdf/README.md)
- Example scripts: [`samples/`](samples/README.md)
    - **Live/manual test scripts:** [`samples/live/`](samples/live/README.md)
- Unit & integration tests: [`tests/`](tests/README.md)
- Docker & environment setup: [`.docker/`](.docker/README.md)

For detailed API documentation, visit the [official iLovePDF API docs](https://developer.ilovepdf.com/docs).

---
