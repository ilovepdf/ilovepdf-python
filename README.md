# iLovePDF API - Python Library

[![PyPI version](https://img.shields.io/pypi/v/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)
[![Python versions](https://img.shields.io/pypi/pyversions/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)
[![License](https://img.shields.io/pypi/l/ilovepdf.svg)](https://pypi.org/project/ilovepdf/)

A Python library for [iLovePDF API](https://developer.ilovepdf.com) to automate PDF processing tasks such as compressing, merging, splitting, converting, protecting, and more.

You can sign up for an iLovePDF account at https://developer.ilovepdf.com

Develop and automate PDF processing tasks like Compress PDF, Merge PDF, Split PDF, convert Office to PDF, PDF to JPG, Images to PDF, add Page Numbers, Rotate PDF, Unlock PDF, stamp a Watermark and Repair PDF. Each one with several settings to get your desired results.

## Requirements

- Python 3.10 to 3.14

## Installation

You can install the library via [PIP](https://pypi.org/project/pip/). Run the following command:

```bash
pip install ilovepdf
```

For other install options (source, pre-release), see [INSTALL.md](INSTALL.md).

## Quick Start

1. Get your API keys from [https://developer.ilovepdf.com](https://developer.ilovepdf.com)
2. Run a task:

```python
from ilovepdf import CompressTask

task = CompressTask(public_key="your_public_key", secret_key="your_secret_key")
task.add_file("document.pdf")
task.execute()
task.download("output_folder")
```

---

## Project Structure & Documentation

- Core library: [`ilovepdf/`](ilovepdf/README.md)
- Example scripts: [`samples/`](samples/README.md)
- Unit & integration tests: [`tests/`](tests/README.md)
- Installation: [`INSTALL.md`](INSTALL.md) - All install options
- Development: [`DEVELOPMENT.md`](DEVELOPMENT.md) - Contributing & setup
- Docker & environment setup: [`.docker/`](.docker/README.md)

For full API docs, visit [developer.ilovepdf.com](https://developer.ilovepdf.com/docs)
