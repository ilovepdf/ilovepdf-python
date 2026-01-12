"""
Provides reusable sample objects for unit and integration tests.

This module defines classes and variables with preconfigured sample instances
(e.g., File, SignTask, UploadTask) to be used across multiple test modules.
These samples help ensure consistency and reduce duplication in test data.

Example:
    from tests.unit.samples_utils import FileSamples, SignTaskSamples

    def test_example():
        file = FileSamples.file1
        sign_task = SignTaskSamples.basic
        # Use samples in test logic
"""

from ilovepdf import File
from ilovepdf.sign import Element, Signer, SignerFile

# pylint: disable=too-few-public-methods,missing-class-docstring


class FileSamples:
    """Reusable sample File objects for testing purposes."""

    file1 = File(server_filename="server_filename1", filename="filename1")
    file2 = File(server_filename="server_filename2", filename="filename2")
    file3 = File(server_filename="server_filename3", filename="filename3")
    file4 = File(server_filename="server_filename4", filename="filename4")

    all_samples = [file1, file2, file3, file4]


class SignElementSamples:
    """Reusable sample Element objects for testing purposes."""

    element1 = Element()
    element2 = Element()
    element3 = Element()
    element4 = Element()

    all_samples = [element1, element2, element3, element4]


class SignerFileSamples:
    signer_file1 = SignerFile(file=FileSamples.file1)
    signer_file2 = SignerFile(file=FileSamples.file2)
    signer_file3 = SignerFile(file=FileSamples.file3)
    signer_file4 = SignerFile(file=FileSamples.file4)
    all_samples = [signer_file1, signer_file2, signer_file3, signer_file4]


class SignerSamples:
    signer1 = Signer(name="John Doe", email="john.doe@example.com")
    signer1.add_file(FileSamples.file1)
    signer1.add_file(FileSamples.file2)
    signer2 = Signer(name="Jane Doe", email="jane.doe@example.com")
    signer2.add_file(FileSamples.file3)
    signer2.add_file(FileSamples.file4)
    all_samples = [signer1, signer2]


sample_classes = (FileSamples, SignElementSamples, SignerFileSamples, SignerSamples)
