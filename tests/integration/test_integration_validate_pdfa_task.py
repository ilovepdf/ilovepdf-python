"""Integration tests for ValidatePdfATask using the iLovePDF API.

This module validates the end-to-end PDF/A compliance validation workflow,
including adding a file, executing the validation, and checking the result.
"""

from ilovepdf.validate_pdfa_task import ValidatePdfATask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestValidatePdfATaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for ValidatePdfATask using the iLovePDF API.

    Covers:
        - Add a PDF sample file to the task.
        - Execute the PDF/A validation workflow.
        - Check the validation result for compliance status.
    """

    task_class = ValidatePdfATask

    def test_pdfa_validation_flow(self) -> None:
        """
        Runs the full PDF/A validation flow from upload to result check.
        """
        self.add_sample_file()

        self.execute_task()

        result = self.task.validation_result
        assert result is not None, (
            "Validation result should not be None after execution."
        )
        assert "status" in result, "Validation result should include 'status' key."
        assert result["status"] in (
            "Conformant",
            "NonConformant",
        ), "'status' should be 'Conformant' or 'NonConformant'."
        # Non-conformant results should include reasons
        if result["status"] == "NonConformant":
            assert "reason" in result, (
                "Non-conformant result should include 'reason' key."
            )
            assert isinstance(result["reason"], list), (
                "'reason' should be a list of strings."
            )
