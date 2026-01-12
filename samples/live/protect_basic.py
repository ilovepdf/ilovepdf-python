"""Real example: protect sample.pdf with password using ProtectTask.
Downloads protected file into output_live/protect_basic_result.pdf.
"""

from ilovepdf import ProtectTask

my_task = ProtectTask()
file = my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.password = "live_sample_password123"
my_task.execute()
my_task.set_output_filename("protect_basic_result.pdf")
my_task.download("output_live")
