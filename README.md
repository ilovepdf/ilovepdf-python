iLovePDF API - Python Library
-----------------------------

[![Latest Stable Version](https://pypi.org/project/ilovepdf-python/)](https://pypi.org/project/ilovepdf-python/)
[![License](https://img.shields.io/pypi/l/ilovepdf-python.svg)](https://pypi.org/project/ilovepdf-python/)

A library in Python for [iLovePDF API](https://developer.ilovepdf.com)

You can sign up for an iLovePDF account at https://developer.ilovepdf.com

Develop and automate PDF processing tasks like Compress PDF, Merge PDF, Split PDF, convert Office to PDF, PDF to JPG, Images to PDF, add Page Numbers, Rotate PDF, Unlock PDF, stamp a Watermark and Repair PDF. Each one with several settings to get your desired results.

## Requirements

Python 3.9+

## Install

You can install the library via [pip](https://pypi.org/project/pip/). Run the following command:

```bash
pip install ilovepdf
```

## Install from source

```bash

virtualenv venv
source venv/bin/activate
pip install -U git+https://github.com/ilovepdf/ilovepdf-python.git@main#egg=ilovepdf


```

To use the library, import it in your Python code:

```python
from ilovepdf import Ilovepdf
```

## Environment Variables

The following environment variable can be set to control logging verbosity:

- `PYTHONLOGLEVEL` – Sets the Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default is `INFO`.

Example usage:

Set the variable for the current shell session:
```bash
export PYTHONLOGLEVEL=DEBUG
python your_script.py
```

Or set it only for a single command:
```bash
PYTHONLOGLEVEL=DEBUG python your_script.py
```

You can also use it with pytest to see more detailed logs during testing:
```bash
PYTHONLOGLEVEL=DEBUG pytest
```

To see all logs and outputs (including print statements and library outputs) in real time during tests, use:
```bash
PYTHONLOGLEVEL=DEBUG pytest --log-cli-level=DEBUG --capture=no
```

## Getting Started

Simple usage looks like:

```python
from ilovepdf import Ilovepdf

ilovepdf = Ilovepdf('project_public_id','project_secret_key')

```

## Samples

See the samples [folder](./samples).

## Docker Support

For development and testing in a consistent environment, you can use Docker.

See [.docker/README.md](.docker/README.md) for full instructions.

## Project Structure

```
ilovepdf-python/
├── ilovepdf/           # Core library source code
├── samples/            # Example scripts demonstrating usage
├── tests/
│   ├── unit/           # Unit tests for individual modules/classes
│   ├── integration/    # Integration tests for API and workflows
│   └── README.md       # Overview of all tests
├── .docker/            # Dockerfiles and compose for development
│   └── README.md       # Docker usage instructions
├── README.md           # Main project documentation
└── ...                 # Other config and documentation files
```

## Links

- [Unit Tests README](tests/unit/README.md)
- [Integration Tests README](tests/integration/README.md)
- [Samples README](samples/README.md)
- [Official iLovePDF API Documentation](https://developer.ilovepdf.com/docs)
