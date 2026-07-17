"""Unit tests for the library version reporting.

These tests verify that the version declared in `ilovepdf/__init__.py` is the
same version used at runtime by the API client and embedded in task request
bodies. This catches stale `.pyc` caches where the runtime version diverges from
the source file.
"""

import re
from pathlib import Path

import ilovepdf
from ilovepdf import CompressTask, Ilovepdf


class TestLibraryVersion:
    """Unit tests for library version propagation."""

    def test_runtime_version_matches_source(self):
        """Runtime __version__ must match the value in __init__.py source.

        This guards against stale bytecode caches where the imported version
        differs from the source file (e.g. after bumping `__version__` without
        clearing `__pycache__`).
        """
        source_path = Path(ilovepdf.__file__)
        source_text = source_path.read_text(encoding="utf-8")
        match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', source_text, re.M)
        assert match is not None, "__version__ not found in ilovepdf/__init__.py"
        source_version = match.group(1)

        assert ilovepdf.__version__ == source_version

    def test_ilovepdf_class_version_matches_package_version(self):
        """Ilovepdf.VERSION must be 'python.' + the package version."""
        assert hasattr(Ilovepdf, "VERSION")
        assert Ilovepdf.VERSION == f"python.{ilovepdf.__version__}"

    def test_task_build_body_includes_library_version(self):
        """Task payloads must include the library version as the 'v' param."""
        task = CompressTask("public_key", "secret_key", make_start=False)
        body = task.build_body()

        assert "params" in body
        assert "v" in body["params"]
        assert body["params"]["v"] == f"python.{ilovepdf.__version__}"
        assert body["params"]["v"] == Ilovepdf.VERSION
