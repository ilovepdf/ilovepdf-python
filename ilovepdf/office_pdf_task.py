"""Module for handling Office to PDF conversion tasks in iLovePDF."""

from .task import ProcessTask

# pylint: disable=abstract-method


class OfficePdfTask(ProcessTask):
    """
    Class to handle the Office to PDF conversion task in iLovePDF.
    """

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="officepdf")

    def _validate_file_extension(self, file_path):
        allowed_extensions = (
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".xls",
            ".xlsx",
            ".odt",
            ".odp",
            ".ods",
        )
        if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(
                "Only Office and OpenDocument files are supported: "
                "DOC, DOCX, PPT, PPTX, XLS, XLSX, ODT, ODP, ODS"
            )

    def add_file(self, file_path, extra_params=None):
        if len(self.files) == 1:
            raise ValueError("OfficePdfTask can only handle one file at a time.")
        self._validate_file_extension(file_path)
        return super().add_file(file_path, extra_params)
