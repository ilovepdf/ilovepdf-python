"""
Sample usage of SignTask for a basic digital signature workflow.

Demonstrates how to use the SignTask class to digitally sign a PDF document using the
iLovePDF API. Due to current API limitations, only basic signer definition is shown (no
custom elements).

For API docs, see: https://developer.ilovepdf.com/docs/api-reference/sign
"""

from ilovepdf import SignTask
from ilovepdf.sign import Signer

# Initialize the signature task with your project keys
sign_task = SignTask("project_public_id", "project_secret_key")

# Add the file to be signed
file = sign_task.add_file("/path/to/file/document.pdf")

# Create and add a signer (basic, only name and email supported via Signer)
signer = Signer(name="Signer Name", email="signer@email.com")
signer.add_file(file)
sign_task.add_signer(signer)

# Optionally set various signature request parameters (see Task properties)
sign_task.subject_signer = "Please sign this document"
sign_task.message_signer = "Hi, please review and sign."
sign_task.lock_order = False
sign_task.language = "en-US"
sign_task.expiration_days = 30
sign_task.uuid_visible = True

# NOTE: File download is not supported for SignTask via the current API.
# To retrieve the result, inspect sign_task after execution or follow API docs.
signature_info = sign_task.execute().result
print(signature_info)
