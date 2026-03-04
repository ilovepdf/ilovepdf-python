# Tests Overview

This directory contains all test code for the **iLovePDF Python** library. Tests are organized to ensure code quality, reliability, and correct integration with the iLovePDF API.

## Structure

- `unit/`
  Contains unit tests for individual modules and classes.
  See [`unit/README.md`](unit/README.md) for details.

- `integration/`
  Contains integration tests that interact with the iLovePDF API and test complete workflows.
  See [`integration/README.md`](integration/README.md) for details.

## Running Tests

You can run tests using [pytest](https://docs.pytest.org/):

```bash
pytest tests/unit
pytest tests/integration
```

Or run all tests at once:

```bash
pytest tests
```

For integration tests, ensure you have set up the required environment variables as described in [`.docker/README.md`](../.docker/README.md).

### Using Docker

To run tests in an isolated environment with multiple Python versions, use Docker Compose:

```bash
docker-compose -f .docker/docker-compose.yml run python310
docker-compose -f .docker/docker-compose.yml run python311
```

See [`.docker/README.md`](../.docker/README.md) for full instructions.

## Coverage

- **Unit tests** cover all core modules and public interfaces.
- **Integration tests** cover end-to-end scenarios and API interactions.

Each new core module or task must include:
- At least one unit test in `unit/`
- At least one integration test in `integration/`

For more information, refer to the README files in each subfolder.

---

## Related Documentation

- [Project Overview](../README.md)
- [Core Library](../ilovepdf/README.md)
- [Samples and Usage](../samples/README.md)
- [Docker and Environment Setup](../.docker/README.md)
