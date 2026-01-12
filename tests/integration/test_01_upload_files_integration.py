"""Test the upload files integration."""

import os
import unittest

from ilovepdf import CompressTask

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestActivityUploadFilesIntegration(BaseIlovePdfTaskTest):
    """Test the upload files integration."""

    sample_file_path = "sample_2MB.pdf"  # Must exist and be >1MB

    task_class = CompressTask  # This can be any valid Task class from iLovePDF

    def test_full_upload_flow(self):
        # 1. Start a new task
        self.assertEqual(self.task.tool, "compress")

        # 2. Upload a PDF file and associate it with the task
        uploaded_file = self.add_sample_file()
        self.assertIsNotNone(
            getattr(uploaded_file, "server_filename", None),
            "Uploaded file should have a server_filename.",
        )

        # 3. Handling of large files (sample file should be larger than 1MB)
        file_size = os.path.getsize(self.sample_file_path)
        self.assertGreater(
            file_size,
            1024 * 1024,
            "Sample file should be larger than 1MB for this test.",
        )

        # 4. Execute the task and download the result
        self.execute_task()
        self.download_result("integration_compressed_sample.pdf")


if __name__ == "__main__":
    unittest.main()
