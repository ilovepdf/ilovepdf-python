# Gitea Workflows - Internal Development Only

> **Note:** These workflows are for the **primary developer's internal Gitea instance**. The public GitHub repository uses separate workflows in `.github/workflows/`.

---

## Architecture: Modular Workflows

This directory uses a **modular architecture** where jobs are defined once and reused across multiple workflows.

```
.gitea/workflows/
├── jobs/                      # Reusable job definitions
│   ├── lint.yml              # Linting (flake8, black, isort, pylint)
│   ├── unit-test.yml         # Unit tests with coverage
│   ├── integration-test.yml  # Integration tests against API
│   └── installation.yml      # Installation validation
│
├── quick.yml                 # Auto: Lint + Unit tests (fast, daily development)
├── integration.yml           # Tag integration-*: Integration tests only
├── installation.yml          # Tag install-*: Installation validation only
├── full.yml                  # Tag full-*: Complete validation (all jobs)
│
├── release-test.yml          # Tag v*-test*: Release to TestPyPI
└── release-production.yml    # Tag v*: Release to PyPI
```

---

## Quick Reference

| Workflow | Trigger | Jobs | Duration |
|----------|---------|------|----------|
| `quick.yml` | Auto (push) | Lint + Unit tests | ~3-5 min |
| `integration.yml` | Tag `integration-*` | Integration tests | ~5-10 min |
| `installation.yml` | Tag `install-*` | Installation validation | ~4-6 min |
| `full.yml` | Tag `full-*` | All jobs (complete) | ~12-18 min |
| `release-test.yml` | Tag `v*-test*` | TestPyPI release | ~5 min |
| `release-production.yml` | Tag `v*` | PyPI release | ~5 min |

---

## Daily Usage

### 1. Normal Development (Automatic - Fast)
```bash
git commit -m "Add watermark feature"
git push
# → quick.yml runs automatically (~3-5 min)
# → Lint + Unit tests (Python 3.10 & 3.14)
```

### 2. Integration Tests Only
```bash
git tag integration-1
git push origin integration-1
# → integration.yml runs (~5-10 min)
# → Integration tests against real API

# Cleanup after:
git push origin --delete integration-1
```

### 3. Installation Validation Only
```bash
git tag install-check
git push origin install-check
# → installation.yml runs (~4-6 min)
# → Validates package installation methods

# Cleanup:
git push origin --delete install-check
```

### 4. Full Validation (Before Release)
```bash
git tag full-v0.2.0-rc1
git push origin full-v0.2.0-rc1
# → full.yml runs (~12-18 min)
# → Lint → Unit → Installation → Integration (all tests)

# Cleanup:
git push origin --delete full-v0.2.0-rc1
```

### 5. Release
```bash
# Test release first
git tag v0.2.0-test1
git push origin v0.2.0-test1
# → Publishes to TestPyPI

# Production release
git tag v0.2.0
git push origin v0.2.0
# → Publishes to PyPI
```

---

## Workflow Details

### `quick.yml` - Fast Daily Development

**Triggers:**
- Automatic on push (only when relevant files change)
- Pull requests

**Runs when these files change:**
- Python files: `*.py`, `ilovepdf/**/*.py`, `tests/**/*.py`, `samples/**/*.py`
- Config files: `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`
- Workflow files: `quick.yml`, `jobs/lint.yml`, `jobs/unit-test.yml`

**Skips when only these change:**
- Documentation: `*.md`
- Docker files: `.docker/**`
- Other workflows

**Jobs:**
1. Lint (Python 3.10)
2. Unit Tests (Python 3.10 & 3.14 in parallel)

---

### `integration.yml` - API Integration Tests

**Triggers:**
- Tags matching `integration-*`

**Requirements:**
- `ILOVEPDF_PUBLIC_KEY` secret
- `ILOVEPDF_SECRET_KEY` secret

**Jobs:**
1. Validate API keys
2. Integration tests (Python 3.10 & 3.14)

**Note:** Tests interact with real iLovePDF API

---

### `installation.yml` - Package Installation

**Triggers:**
- Tags matching `install-*`

**Jobs:**
1. Global installation validation
2. User installation validation
3. VCS installation from git

**Tests:**
- Python 3.10 & 3.14

---

### `full.yml` - Complete Validation

**Triggers:**
- Tags matching `full-*`

**Requirements:**
- All secrets must be configured

**Jobs (in order):**
1. Lint
2. Unit Tests (3.10 & 3.14 in parallel)
3. Installation Validation (3.10 & 3.14 in parallel)
4. Validate API Keys
5. Integration Tests (3.10 & 3.14 in parallel)

**Use before:**
- Creating releases
- Major pull requests
- After significant refactoring

---

## Configuration

### Python Versions
- **Min:** 3.10
- **Max:** 3.14
- All workflows test both versions

### Fail-Fast Strategy
- All matrix jobs use `fail-fast: true`
- If one Python version fails, others are cancelled immediately
- Saves time and provides faster feedback

### Required Secrets
Set in Gitea repository settings → Secrets:
- `ILOVEPDF_PUBLIC_KEY` - For integration tests
- `ILOVEPDF_SECRET_KEY` - For integration tests

Get keys at: https://developer.ilovepdf.com/user/projects

---

## Modular Jobs

Each job is defined once in `jobs/` and reused across workflows:

### `jobs/lint.yml`
- Flake8 style checking
- Black formatting verification
- isort import sorting
- Pylint code quality (min score: 8.0)

### `jobs/unit-test.yml`
- Pytest unit tests
- Code coverage (min: 85%)
- Timeout: 30 seconds per test
- Coverage reports (XML + terminal)

### `jobs/integration-test.yml`
- Integration tests against iLovePDF API
- Requires API credentials
- Timeout: 60 seconds per test
- Real API interaction

### `jobs/installation.yml`
- Global installation (`pip install`)
- User installation (`pip install --user`)
- VCS installation (`pip install git+...`)
- Import verification

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `quick.yml` doesn't run | Only docs changed | Expected behavior (docs don't trigger CI) |
| Integration tests skip | Tag doesn't match pattern | Use `integration-*` pattern |
| Integration tests fail immediately | Missing secrets | Configure `ILOVEPDF_PUBLIC_KEY` and `ILOVEPDF_SECRET_KEY` |
| One Python version fails, other cancelled | `fail-fast: true` | Fix the issue and re-run the workflow |
| Installation tests fail | Script path issue | Check `.github/workflows/scripts/install_and_verify.sh` exists |
| Full workflow takes too long | All jobs run sequentially | Expected (~12-18 min for complete validation) |

---

## Best Practices

1. **Daily development:** Push frequently, let `quick.yml` catch issues early (~3-5 min)
2. **Before PRs:** Run `full-*` tag to validate everything (~12-18 min)
3. **API changes:** Run `integration-*` tag to test against real API (~5-10 min)
4. **Installation changes:** Run `install-*` tag to validate package installation (~4-6 min)
5. **Clean up tags:** Delete test tags after use to keep repository clean
6. **Monitor times:** If workflows slow down, optimize or parallelize jobs

---

## Comparison: Modular vs Monolithic

**Before (Monolithic):**
- Single `ci.yml` with all jobs inline
- Changes require editing large file
- Can't run individual validations
- Code duplication across workflows

**After (Modular):**
- Jobs defined once in `jobs/`
- Workflows compose jobs as needed
- Run exactly what you need (granular control)
- No code duplication
- Easy to maintain and extend

---

## For Contributors

These internal workflows **do not affect public contributions**. 

Focus on the public GitHub repository workflows in `.github/workflows/`.

Your PR must pass the public CI/CD pipeline.

---

**Maintainer:** Internal use only for primary development  
**Last Updated:** 2025-01-11