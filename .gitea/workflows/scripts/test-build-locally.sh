#!/bin/bash

# test-build.sh - Local build and test script for ilovepdf-python
# Builds the package, runs a local pypiserver, uploads, and tests installation

set -e  # Exit on error

echo "=== ilovepdf-python Local Build Test ==="

# Clean pip cache first
echo "Cleaning pip cache..."
pip cache purge 2>/dev/null || true

# Install required tools
echo "Installing build tools..."
pip install pypiserver build twine > /dev/null 2>&1

# Create packages directory
mkdir -p packages
rm -rf packages/*

# Create dist directory
mkdir -p dist
rm -rf dist/*

# Start local pypiserver
echo "Starting local pypiserver on port 8080..."
pypi-server run -p 8080 -P . -a . packages > /dev/null 2>&1 &
PYPISERVER_PID=$!

# Wait for server to start
sleep 3
if ! curl -s http://localhost:8080 > /dev/null; then
    echo "Error: Pypiserver failed to start"
    kill $PYPISERVER_PID 2>/dev/null || true
    exit 1
fi
echo "✓ Pypiserver ready"

# Build package
echo "Building package..."
python -m build

# Upload to local pypiserver
echo "Uploading to local pypiserver..."
twine upload --repository-url http://localhost:8080 --non-interactive --username "" --password "" dist/*

# Test installation - force reinstall
echo "Testing installation..."
pip install --force-reinstall --no-cache-dir --index-url http://localhost:8080/simple ilovepdf

# Verify installation
echo "Verifying package..."
python -c "
from ilovepdf import Ilovepdf
print('✓ Successfully imported Ilovepdf class')
print('✓ Build and test completed successfully')
"

# Cleanup
echo "Stopping pypiserver..."
kill $PYPISERVER_PID 2>/dev/null || true

echo "=== ✅ Test completed successfully ==="
