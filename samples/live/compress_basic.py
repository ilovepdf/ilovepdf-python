"""Real example: compress a PDF file using CompressTask (sample.pdf).

Uses tests/integration/files_samples/sample.pdf as input and downloads result
into output_live/.
"""

from ilovepdf import CompressTask

# Uses env vars if credentials omitted
my_task = CompressTask()

# Add PDF file to compress
file = my_task.add_file("tests/integration/files_samples/sample.pdf")

# Process the task
my_task.execute()

# Download the compressed output file into output_live/
my_task.set_output_filename("compress_basic_sample.pdf")
my_task.download("output_live")
