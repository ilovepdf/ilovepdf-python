"""ExtendedException module for iLovePDF Python API.

This module defines the ExtendedException class, which stores additional error
information from API responses.
"""


class ExtendedException(Exception):
    """
    ExtendedException for iLovePDF Python API.
    Stores additional error information from API responses.
    """

    def __init__(self, message, response_body=None, code=0, previous=None):
        super().__init__(message)
        self.params = None
        self.type = None
        self.code = code
        self.previous = previous

        if response_body:
            # Expecting response_body as a dict (from json)
            error = (
                response_body.get("error", {})
                if isinstance(response_body, dict)
                else {}
            )
            self.type = error.get("type")
            self.params = error.get("param")

            if self.params:
                if isinstance(self.params, list):
                    first_error = self._get_first_error(self.params[0])
                else:
                    first_error = self._get_first_error(self.params)
                self.args = (f"{message} ({first_error})",)
            else:
                if "message" in error:
                    self.args = (f"{message} ({error['message']})",)
                else:
                    self.args = (message,)

    def _get_first_error(self, error):
        if isinstance(error, dict):
            # Recursively get first string error
            for value in error.values():
                return self._get_first_error(value)
        elif isinstance(error, str):
            return error
        elif isinstance(error, list) and error:
            return self._get_first_error(error[0])
        return str(error)

    def get_errors(self):
        """
        Returns the error parameters from the API response.

        Returns:
            list or dict: The error parameters if available, otherwise an empty list.
        """
        if not isinstance(self.params, (list, dict)):
            return []
        return self.params

    def get_type(self):
        """
        Returns the error type from the API response.

        Returns:
            str or None: The error type if available, otherwise None.
        """
        return self.type
