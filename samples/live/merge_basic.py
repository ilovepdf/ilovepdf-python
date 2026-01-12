"""Real example: merge two PDFs using MergeTask.
Uses sample PDFs from tests/integration/files_samples/ and downloads result into
output_live/merge_basic_result.pdf.
"""

from ilovepdf import MergeTask

my_task = MergeTask()
file1 = my_task.add_file("tests/integration/files_samples/sample.pdf")
file2 = my_task.add_file("tests/integration/files_samples/sample.pdf")

my_task.execute()
my_task.set_output_filename("merge_basic_result.pdf")
my_task.download("output_live")
