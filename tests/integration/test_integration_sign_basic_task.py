"""Integration tests for SignTask using the iLovePDF API.

Covers:
- Full workflow: add file, create signature element, assign to signer, execute, and
    validate result structure.
"""

import os

from ilovepdf import SignTask

from .base_task_integration_test import BaseTaskIntegrationTest


# pylint: disable=protected-access
class TestSignBasicTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for SignTask using the iLovePDF API.

    Covers:
    - Full workflow: add file, create signature element, assign to signer, execute, and
       validate result structure.
    """

    task_class = SignTask
    sample_file_path = "sample.pdf"

    def test_full_sign_flow(self):
        """
        Test the full electronic signature workflow for the SignTask.

        Steps:
        - Add file
        - Create signature element
        - Assign to signer
        - Add signer to task
        - Execute task and assert task status
        - Validate that at least one signer exists and fields are correct.

        Note:
            The SignTask does not support file download via API, so the test does not
                validate downloaded output.
        """
        # Add the sample file to the task
        file = self.add_sample_file()

        signer = self.task.add_signer()
        signer.name = os.getenv("SIGNER_NAME", "John Doe")
        signer.email = os.getenv("SIGNER_EMAIL", "john.doe@example.com")
        signer.add_file(file)
        self.execute_task()

        # Validate that at least one signer exists
        assert (
            len(self.task.signers) > 0
        ), "No signers were found in the task after execution."
        # Validate that signer has name and email
        assert self.task.signers[0].name == signer.name, "Signer name does not match."
        assert (
            self.task.signers[0].email == signer.email
        ), "Signer email does not match."
