#!/usr/bin/env python3
"""
Verifies that the ilovepdf package is installed in the expected location.

Usage:
    python verify_install.py global
    python verify_install.py user

Arguments:
    global  - Checks that ilovepdf is installed in site-packages or dist-packages.
    user    - Checks that ilovepdf is installed in the user site (.local).

Exits with code 1 if the package is not found in the expected location.
"""

import sys


def check_import(expected_path):
    try:
        import ilovepdf

        ilovepdf_path = ilovepdf.__file__
        print(f"Install location: {ilovepdf_path}")
        if expected_path not in ilovepdf_path:
            print(f"ERROR: Not installed in {expected_path}")
            sys.exit(1)
    except ImportError:
        print("ERROR: ilovepdf package not found.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_install.py [global|user]")
        sys.exit(2)
    mode = sys.argv[1]
    if mode == "global":
        # Accept either site-packages or dist-packages
        check_import("site-packages")
    elif mode == "user":
        check_import(".local")
    else:
        print("Unknown mode. Use 'global' or 'user'.")
        sys.exit(2)
