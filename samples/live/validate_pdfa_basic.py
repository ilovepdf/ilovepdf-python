"""Real example: validate PDF/A compliance of sample.pdf using ValidatePdfATask.
Prints the validation status and reasons if non-conformant.
"""

from ilovepdf import ValidatePdfATask

my_task = ValidatePdfATask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.execute()

result = my_task.validation_result
if result is not None:
    print(f"Status: {result.get('status')}")
    if result.get("status") == "NonConformant":
        for reason in result.get("reason", []):
            print(f"  - {reason}")
else:
    print("No validation result available.")
