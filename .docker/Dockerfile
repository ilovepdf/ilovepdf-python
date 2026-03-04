ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Set working directory
WORKDIR /src

# Set Python environment variables early to prevent .pyc creation during build
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy project configuration files first (rarely change)
COPY pyproject.toml ./
COPY requirements.txt requirements_dev.txt requirements_test.txt ./

# Upgrade pip and install test dependencies as root
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_test.txt

# Copy source code and tests
COPY ilovepdf ./ilovepdf
COPY tests ./tests

# Install the package system-wide (non-editable) before switching to non-root
RUN pip install .

# Change ownership to appuser and switch user
RUN chown -R appuser:appuser /src
USER appuser

# Update PATH for user-installed packages
ENV PATH="/home/appuser/.local/bin:$PATH"

# Install package in user site to validate non-root installs
RUN pip install --user .

RUN rm -rf ilovepdf

# Verify imports resolve from user site in normal mode (outside project workspace)
RUN cd / && PYTHONPATH="" python - <<'PY'
import ilovepdf
p = ilovepdf.__file__
print(p)
assert '.local' in p, 'User-site install not used in normal mode.'
PY

# Verify imports come from the system installed package in isolated mode
RUN python -I - <<'PY'
import ilovepdf
p = ilovepdf.__file__
print(p)
assert ('site-packages' in p) or ('dist-packages' in p), \
    'Package not imported from system installation.'
PY

# Default command: run unit tests; integration requires API secrets to be provided
CMD ["sh", "-c", "\
    pytest tests/unit \
        --cov=ilovepdf \
        --cov-report=xml \
        --cov-report=term \
        --cov-fail-under=85 \
        --timeout=30 \
        -v \
        --tb=short \
    && pytest tests/integration"]
