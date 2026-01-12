## Development with Docker

This directory contains Docker configuration files for developing and testing the iLovePDF Python library in an isolated environment.

Due to a limitation in `docker-compose` when handling `docker-compose.yml` files in subdirectories, the build and run process is separated into two steps.

### 1. Build the Docker Image

To build the docker image, run the following command from the project root:

```bash
docker build -t ilovepdf-python39 -f .docker/Dockerfile .
```

**To force a rebuild (ignore cache), use:**

```bash
docker build --no-cache -t ilovepdf-python39 -f .docker/Dockerfile .
```

For general project usage and documentation, see [../README.md](../README.md).

---

## Environment Variables

To run integration tests and use the API, you must set the following environment variables.
Copy `.env.sample` to `.env` and fill in your credentials:

```bash
cp .docker/.env.sample .docker/.env
```

Edit `.docker/.env` and set:

- `ILOVEPDF_PUBLIC_KEY` – Your iLovePDF project public key
- `ILOVEPDF_SECRET_KEY` – Your iLovePDF project secret key
- `FOLDER_SAMPLE_PATH` – Path to sample files (default: `tests/integration/files_samples`)

These variables are required for integration tests and API usage.

You need to re-run this command every time you make changes to the source code or the `Dockerfile`.

### 2. Run the Services

To run the services, use the following `docker-compose` command:

```bash
docker-compose -f .docker/docker-compose.yml up
```
