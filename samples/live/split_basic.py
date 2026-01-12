"""Real example: split sample.pdf using SplitTask (ranges 2-4, 6-8).
Downloads ZIP file with split PDFs into output_live/split_basic_result.zip.
"""

from ilovepdf import SplitTask

my_task = SplitTask()
file = my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.ranges = "2-4,6-8"
my_task.execute()
my_task.set_output_filename("split_basic_result.zip")
my_task.download("output_live")
