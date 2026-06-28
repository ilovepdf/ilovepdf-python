"""Handles PDF to Markdown conversion tasks using the iLovePDF API.

Provides the PdfMarkdownTask class to convert PDF files into Markdown format.
"""

from .task import Task


class PdfMarkdownTask(Task):
    """
    Handles PDF to Markdown conversion tasks using the iLovePDF API.

    Converts PDF files into Markdown text format.

    Example:
        task = PdfMarkdownTask(
            public_key="your_public_key", secret_key="your_secret_key"
        )
        task.add_file("/path/to/document.pdf")
        task.execute()
        task.download("/path/to/output.md")
    """

    _tool = "pdfmarkdown"
