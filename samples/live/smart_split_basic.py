"""Live example: AI-powered smart split using SmartSplitTask.

This script demonstrates splitting a PDF based on content analysis.
Downloads the result (a ZIP with split PDFs) to output_live/.
"""

from ilovepdf import SmartSplitTask

my_task = SmartSplitTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.prompt = "Split at chapter boundaries"
my_task.execute()
my_task.set_output_filename("smart_split_basic_result.zip")
my_task.download("output_live")
