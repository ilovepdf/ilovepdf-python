"""Real example: extract text from sample.pdf using ExtractTask.
Downloads text file into output_live/extract_basic_result.txt.
"""

from ilovepdf import ExtractTask

my_task = ExtractTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.detailed = True
my_task.execute()
my_task.set_output_filename("extract_basic_result.txt")
my_task.download("output_live")
