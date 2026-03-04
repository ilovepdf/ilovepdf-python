# Gitea Workflows - Internal Development Only

> **Note:** These workflows are for the **primary developer's internal Gitea
> instance**. Public contributions should focus on `.github/workflows/`.

---

## Architecture

Jobs are defined once in `jobs/` and reused across workflows. Scripts used by
jobs live in `scripts/`. A composite Telegram action lives in
`.gitea/actions/notify-telegram/`.

```
.gitea/
├── actions/
│   └── notify-telegram/       # Composite action for Telegram messages
│       └── action.yaml
│
└── workflows/
    ├── scripts/                   # Shared scripts for jobs
    │   ├── install_and_verify.sh  # pip install + location check
    │   └── verify_install.py      # Validates import location
    │
    ├── jobs/                      # Reusable job definitions
    │   ├── lint.yml               # black, ruff, pyright
    │   ├── unit-test.yml          # pytest + coverage (min 85%)
    │   ├── integration-test.yml   # Tests against real iLovePDF API
    │   ├── installation.yml       # pip install validation (global, user, VCS)
    │   ├── validate-secrets.yml   # Checks API key secrets are configured
    │   └── notify-telegram.yml    # Sends success/failure Telegram notification
    │
    ├── quick.yml                  # Auto: Lint + Unit tests
    ├── integration.yml            # Tag integration-*: Integration tests
    ├── installation.yml           # Tag install-*: Installation validation
    ├── full.yml                   # Tag full-*: All jobs
    │
    ├── release-test.yml           # Tag v*-test*: Release to TestPyPI
    └── release-production.yml     # Tag v*: Release to PyPI
```

---

## Quick Reference

| Workflow | Trigger | Jobs | Notifications | Duration |
|----------|---------|------|:---:|----------|
| `quick.yml` | Push (auto) | Lint → Unit tests | ✅ | ~1-2 min |
| `integration.yml` | Tag `integration-*` | Validate secrets → Integration tests | ✅ | ~5-10 min |
| `installation.yml` | Tag `install-*` | Installation validation | ✅ | ~50 sec |
| `full.yml` | Tag `full-*` | All jobs (complete) | ✅ | ~5-10 min |
| `release-test.yml` | Tag `v*-test*` | TestPyPI release | ✅ | ~10-20 sec |
| `release-production.yml` | Tag `v*` | PyPI release | ✅ | ~10-20 sec |

---

## Daily Usage

### 1. Normal Development (automatic)

```bash
git push
# → quick.yml: Lint + Unit tests (~1-2 min)
```

### 2. Integration Tests

```bash
git tag integration-1 && git push origin integration-1
# → integration.yml (~5-10 min)

# Cleanup:
git push origin --delete integration-1
```

### 3. Installation Validation

```bash
git tag install-check && git push origin install-check
# → installation.yml (~50 sec)

# Cleanup:
git push origin --delete install-check
```

### 4. Full Validation (before release)

```bash
git tag full-v0.2.0-rc1 && git push origin full-v0.2.0-rc1
# → full.yml: Lint → Unit → Installation → Integration (~5-10 min)

# Cleanup:
git push origin --delete full-v0.2.0-rc1
```

### 5. Release

```bash
# Test release
git tag v0.2.0-test1 && git push origin v0.2.0-test1
# → Publishes to TestPyPI

# Production release
git tag v0.2.0 && git push origin v0.2.0
# → Publishes to PyPI
```

---

## Configuration

### Python Versions

- **Min:** 3.10 | **Max:** 3.14
- All workflows test both versions.
- `fail-fast: true` — if one version fails, others are cancelled immediately.

### Required Secrets

Set in Gitea → Repository Settings → Secrets:

| Secret | Used by |
|--------|---------|
| `ILOVEPDF_PUBLIC_KEY` | Integration tests |
| `ILOVEPDF_SECRET_KEY` | Integration tests |
| `TELEGRAM_BOT_TOKEN` | All workflows (notifications) |
| `TELEGRAM_CHAT_ID` | All workflows (notifications) |
| `PYPI_TOKEN` | Production release |
| `TEST_PYPI_TOKEN` | Test release |

Get iLovePDF keys at: https://developer.ilovepdf.com/user/projects

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `quick.yml` doesn't run | Only docs changed | Expected (docs don't trigger CI) |
| Integration tests skip | Tag doesn't match | Use `integration-*` pattern |
| Integration tests fail | Missing secrets | Configure API keys in secrets |
| One Python version fails, other cancelled | `fail-fast: true` | Fix the issue and re-run |
| Installation tests fail | Script path issue | Check `.gitea/workflows/scripts/install_and_verify.sh` |
| Full workflow too slow | Sequential jobs | Expected (~12-18 min) |
| No Telegram notifications | Missing secrets | Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` |

---

**Last Updated:** 2025-03-02
