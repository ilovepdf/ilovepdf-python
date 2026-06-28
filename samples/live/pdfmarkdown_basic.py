"""Live example: convert a PDF to Markdown using PdfMarkdownTask.

This script demonstrates converting a PDF document to Markdown text.
Downloads the result to output_live/pdfmarkdown_basic_result.md.
"""

from ilovepdf import PdfMarkdownTask

my_task = PdfMarkdownTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.execute()
my_task.set_output_filename("pdfmarkdown_basic_result.md")
my_task.download("output_live")
