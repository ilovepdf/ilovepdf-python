"""Real example: repair sample.pdf using RepairTask.
Downloads repaired file into output_live/repair_basic_result.pdf.
"""

from ilovepdf import RepairTask

my_task = RepairTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.execute()
my_task.set_output_filename("repair_basic_result.pdf")
my_task.download("output_live")
