"""Real example: split and merge sample.pdf using SplitTask (advanced).
Downloads merged result to output_live/split_advanced_merge_result.pdf.
"""

from ilovepdf import SplitTask

my_task = SplitTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.ranges = "2-4,6-8"
my_task.merge_after = True
my_task.execute()
my_task.set_output_filename("split_advanced_merge_result.pdf")
my_task.download("output_live")
