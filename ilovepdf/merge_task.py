"""
Handles PDF merge tasks using the iLovePDF API.

Provides the MergeTask class to configure and execute PDF merging operations.
Allows combining multiple PDF files into a single document programmatically via the
iLovePDF API.
"""

from .task import Task


class MergeTask(Task):
    """
    Handles merging of multiple PDF files into one document using the iLovePDF API.

    The MergeTask class allows you to add PDF files and execute a merge process.
    It supports configuration for automated merging workflows and can be integrated
    into batch PDF processing scripts.

    Example:
        merge_task = MergeTask(public_key, secret_key)
        merge_task.add_file('file1.pdf')
        merge_task.add_file('file2.pdf')
        merge_task.execute()
        merge_task.download('merged.pdf')
    """

    _tool = "merge"
