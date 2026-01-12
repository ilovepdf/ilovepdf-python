"""Custom exception for missing or empty required fields in payloads.

Defines MissingPayloadFieldError for use when validating required fields
in API payloads for ilovepdf-python elements and tasks.
"""


class MissingPayloadFieldError(ValueError):
    """Raised when required fields are missing or empty in the payload.

    Args:
        missing_fields (list[str]): List of missing or empty field names.

    Example:
        raise MissingPayloadFieldError(["name", "address"])
    """

    def __init__(self, missing_fields: list[str]):
        fields_str = ", ".join(missing_fields)
        message = f"Missing or empty required field(s): {fields_str}."
        super().__init__(message)
        self.missing_fields = missing_fields
