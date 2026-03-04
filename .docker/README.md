# Docker Setup Guide

Use Docker to test the **iLovePDF Python** library across multiple Python versions (3.10 to 3.14) in isolated environments.

---

## Quick Start

### 1. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API credentials from [iLovePDF Developer Portal](https://developer.ilovepdf.com/user/projects):

```bash
ILOVEPDF_PUBLIC_KEY=your_public_key_here
ILOVEPDF_SECRET_KEY=your_secret_key_here
```

**Important:** Never commit `.env` with real credentials.

---

### 2. Build Images

```bash
docker-compose -f .docker/docker-compose.yml build
```

---

### 3. Run Tests

```bash
docker-compose -f .docker/docker-compose.yml run --rm python310
```

---

## Common Commands

### Run Specific Test Types

```bash
# Unit tests only
docker-compose -f .docker/docker-compose.yml run --rm python310 pytest tests/unit

# Integration tests only
docker-compose -f .docker/docker-compose.yml run --rm python310 pytest tests/integration

# Specific test file
docker-compose -f .docker/docker-compose.yml run --rm python310 pytest tests/unit/test_compress_task.py
```

### Test Different Python Versions

Available: `python310`, `python311`, `python312`, `python313`, `python314`

```bash
docker-compose -f .docker/docker-compose.yml run --rm python312 pytest tests/unit
```

### Rebuild After Code Changes

```bash
docker-compose -f .docker/docker-compose.yml build python310
```

### Rebuild from Scratch

```bash
docker-compose -f .docker/docker-compose.yml build --no-cache python310
```

### Open Shell Inside Container

```bash
docker-compose -f .docker/docker-compose.yml run --rm python310 bash
```

---

## Troubleshooting

### TTY Error

If you see "the input device is not a TTY", add `-T` flag:

```bash
docker-compose -f .docker/docker-compose.yml run --rm -T python310 pytest tests/unit
```

### Import Errors After Code Changes

Rebuild the image:

```bash
docker-compose -f .docker/docker-compose.yml build python310
```

### Authentication Errors

- Verify `.env` file exists in project root with valid credentials
- Check you copied it from `.env.example`
- Integration tests require valid API credentials

---

## Additional Information

- Main documentation: [../README.md](../README.md)
- API docs: [developer.ilovepdf.com/docs](https://developer.ilovepdf.com/docs)
