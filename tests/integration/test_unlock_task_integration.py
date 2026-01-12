"""Integration tests for UnlockTask using the iLovePDF API.

Covers:
- Full workflow: add password-protected file, execute unlock, and download unlocked PDF.
"""

import unittest

from ilovepdf import UnlockTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestUnlockTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for UnlockTask using the iLovePDF API.

    Covers:
    - Full workflow: add password-protected file, execute unlock, and download unlocked PDF.
    """

    task_class = UnlockTask
    sample_file_path = (
        "sample_protected_mysecret.pdf"  # Must be password-protected and present
    )

    def test_full_unlock_flow(self):
        """
        Test the full flow: add protected file, execute unlock, and download.
        """
        # Add the protected sample file to the task
        self.add_sample_file()

        # Execute the unlock task and check status
        self.execute_task()

        # Download the unlocked file and verify
        self.download_result("sample_protected_mysecret_unlocked.pdf")

        # Optionally, you could use a PDF library to check that the file is no longer password-protected.


if __name__ == "__main__":
    unittest.main()
