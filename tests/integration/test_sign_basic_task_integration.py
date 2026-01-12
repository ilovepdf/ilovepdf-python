"""Integration tests for SignTask using the iLovePDF API.

Covers:
- Full workflow: add file, create signature element, assign to signer, execute, and validate result structure.
"""

import unittest
from typing import Any, Dict, List

from ilovepdf import SignTask
from ilovepdf.sign.elements.element_signature import ElementSignature
from ilovepdf.sign.receivers.signer import Signer

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestSignBasicTaskIntegration(BaseIlovePdfTaskTest):
    """
    Integration tests for SignTask using the iLovePDF API.

    Covers:
    - Full workflow: add file, create signature element, assign to signer, execute, and validate result structure.
    """

    task_class = SignTask
    sample_file_path = "sample.pdf"

    def test_full_sign_flow(self):
        """
        Test the full electronic signature flow:
        - Add file
        - Create signature element
        - Assign to signer
        - Add signer to task
        - Execute and validate result
        """
        # Add the sample file to the task
        file = self.add_sample_file()
        self.assertIsNotNone(file, "Failed to add sample file to SignTask.")

        # Create the signature element and configure it
        signature_element = ElementSignature()
        signature_element.set_position(20, -20).set_pages("1").set_size(40)

        # Create a signer and assign the signature element
        signer = Signer("Daniel Mattos", "daniel.mattos@crombie.dev")
        signer.add_elements(file, signature_element)

        # Add the signer to the task
        self.task.add_receiver(signer)

        # Execute the task and check status
        self.task.execute()
        status = getattr(self.task, "status", None)
        status_message = getattr(self.task, "status_message", "")
        self.assertEqual(
            status,
            "draft",
            f"SignTask failed with status: {status} and message: {status_message}",
        )

        # Validate the result structure
        result = getattr(self.task, "result", None)
        self.assertIsNotNone(result, "No result returned from SignTask execution.")

        if not isinstance(result, dict):
            self.fail(f"Result is not a dict, cannot check structure: {result}")

        # Type annotation to help linter understand result is a Dict after the check
        result_dict: Dict[str, Any] = result

        # Top-level fields
        for field in ["status", "signers", "files", "uuid", "created", "email", "name"]:
            self.assertIn(field, result_dict, f"Missing field '{field}' in result.")

        # Check signers list
        signers_raw = result_dict.get("signers", [])
        signers: List[Dict[str, Any]] = (
            signers_raw if isinstance(signers_raw, list) else []
        )
        self.assertIsInstance(signers, list)
        if signers:
            signer_info = signers[0]
            for field in ["uuid", "name", "email", "status"]:
                self.assertIn(
                    field, signer_info, f"Missing field '{field}' in signer info."
                )

        # Check files list
        files_raw = result_dict.get("files", [])
        files: List[Dict[str, Any]] = files_raw if isinstance(files_raw, list) else []
        self.assertIsInstance(files, list)
        if files:
            file_info = files[0]
            for field in ["filename", "pages", "filesize"]:
                self.assertIn(
                    field, file_info, f"Missing field '{field}' in file info."
                )


if __name__ == "__main__":
    unittest.main()
