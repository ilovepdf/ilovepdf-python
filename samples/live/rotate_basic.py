"""Real example: rotate sample.pdf by 90 degrees using RotateTask.
Downloads PDF file into output_live/rotate_basic_result.pdf.
"""

from ilovepdf import RotateTask

my_task = RotateTask()
file = my_task.add_file("tests/integration/files_samples/sample.pdf")
file.rotate = 90
my_task.execute()
my_task.set_output_filename("rotate_basic_result.pdf")
my_task.download("output_live")
