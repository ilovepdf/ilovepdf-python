# Development Guide

## Setup

1. Clone the repository:
```bash
git clone https://github.com/ilovepdf/ilovepdf-python.git
cd ilovepdf-python
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements_dev.txt
pip install -e .
```

> The `-e .` flag installs the package in editable mode.

## Pyright Configuration

Create `pyrightconfig.json` in the project root:

```json
{
  "extraPaths": ["/path/to/lib/python/site-packages"]
}
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `ILOVEPDF_PUBLIC_KEY` - Your API public key
- `ILOVEPDF_SECRET_KEY` - Your API secret key

Optional variables:
- `PYTHONLOGLEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `FOLDER_SAMPLE_PATH` - Path to sample files for testing

## Running Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests (requires API keys)
pytest tests/integration/

# All tests
pytest tests/
```

## Code Style

The project uses:
- **Black** for formatting
- **Ruff** for fast linting and formatting
- **Pyright** for static type checking

Run formatting and linting:
```bash
black .
ruff check .
ruff format .
pyright ilovepdf/
```

For pre-commit hooks (autom

## Adding a New Task

1. Create `ilovepdf/newtask_task.py` extending `Task`
2. Add unit tests in `tests/unit/`
3. Add integration test in `tests/integration/`
4. Add sample script in `samples/`
5. Update `ilovepdf/__init__.py` to export the task

## Project Structure

```
ilovepdf-python/
├── ilovepdf/           # Core library
│   ├── *task.py        # Task implementations
│   ├── task.py         # Base task class
│   ├── exceptions/     # Custom exceptions
│   └── validators/     # Input validators
├── samples/            # Usage examples
├── tests/              # Unit & integration tests
├── .docker/            # Docker configurations
├── README.md           # Main documentation
├── INSTALL.md          # Installation guide
└── DEVELOPMENT.md      # This file
```

## Docker

Build and run tests in Docker using `docker-compose`:

```bash
# Build images
docker-compose -f .docker/docker-compose.yml build

# Run tests with a specific Python version
docker-compose -f .docker/docker-compose.yml run --rm python310 pytest tests/unit

# Run all tests
docker-compose -f .docker/docker-compose.yml run --rm python310 pytest tests/
```

Available Python versions: `python310`, `python311`, `python312`, `python313`, `python314`

For full Docker instructions, see [`.docker/README.md`](.docker/README.md).

## Getting Help

- Issues: https://github.com/ilovepdf/ilovepdf-python/issues
- API Docs: https://developer.ilovepdf.com/docs
