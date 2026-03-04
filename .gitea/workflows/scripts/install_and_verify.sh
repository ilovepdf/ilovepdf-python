#!/bin/bash
# install_and_verify.sh
# Installs ilovepdf package globally or as user, then verifies import location.
# Usage: install_and_verify.sh [global|user]

set -e

MODE="$1"
if [ "$MODE" = "global" ]; then
    pip uninstall -y ilovepdf || true
    pip install .
elif [ "$MODE" = "user" ]; then
    pip uninstall -y ilovepdf || true
    pip install --user .
else
    echo "Usage: $0 [global|user]"
    exit 1
fi

location=$PWD
mkdir -p /tmp/empty
cd /tmp/empty
python $location/.gitea/workflows/scripts/verify_install.py "$MODE"
