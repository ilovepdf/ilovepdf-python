"""Integration tests for UnlockTask using the iLovePDF API.

Covers:
- Full workflow: add password-protected file, execute unlock, and download unlocked PDF.
"""

from ilovepdf import UnlockTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestUnlockTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for UnlockTask using the iLovePDF API.

    Covers:
    - Full workflow: add password-protected file, execute unlock, and download unlocked
        PDF.
    """

    task_class = UnlockTask

    def test_full_unlock_flow(self):
        """
        Test the full flow: add protected file, execute unlock, and download.
        """
        # Add the protected sample file to the task
        self.add_sample_file("sample_protected_mysecret.pdf")

        # Execute the unlock task and check status
        self.execute_task()

        # Download the unlocked file and verify
        self.download_result("sample_protected_mysecret_unlocked.pdf")
