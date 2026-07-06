"""Live example: AI-powered PDF summarization using SummarizeTask.

This script demonstrates generating an AI summary of a PDF document.
Downloads the summarized file to output_live/summarize_basic_result.pdf.
"""

from ilovepdf import SummarizeTask

my_task = SummarizeTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.language = "en"
my_task.output_format = "pdf"
my_task.execute()
my_task.set_output_filename("summarize_basic_result.pdf")
my_task.download("output_live")
