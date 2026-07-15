"""
Advanced usage of SignTask for digital signature workflows.

This example demonstrates how to use the SignTask class with multiple signers.
Applies supported API: no custom elements, receivers or brand/logo signatures (those
features aren't available in the public Python SDK as of now).

For updated API docs, see: https://www.iloveapi.com/docs/api-reference#create-signature
"""

from ilovepdf import SignTask
from ilovepdf.sign import Signer  # Only available class for signers in public SDK

# Initialize the signature task with your keys
sign_task = SignTask("project_public_id", "project_secret_key")

# Add the file to be signed
file = sign_task.add_file("/path/to/file/document.pdf")

# Optionally, set general options
sign_task.lock_order = False
sign_task.language = "en-US"
sign_task.uuid_visible = True
sign_task.expiration_days = 90
sign_task.subject_signer = "Important: Sign digital contract"
sign_task.message_signer = "Please sign this digital contract within 90 days."

# Add multiple signers
signers = [
    Signer(name="Signer One", email="signer1@email.com"),
    Signer(name="Signer Two", email="signer2@email.com"),
]
for signer in signers:
    signer.add_file(file)
    sign_task.add_signer(signer)

# Execute the task (no download, result information is shown after execution)
signature_info = sign_task.execute().result
print(signature_info)
