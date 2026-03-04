"""StringValidator provides validation for string values.

Ensures that a value is of type str and/or is not an empty string.
"""


class StringValidator:
    """Validator for string values.

    Provides static methods to validate that a value is a string and/or not
    empty.

    Methods:
        validate_type:
            Validates that the value is a string.

        validate_not_empty:
            Validates that the string is not empty.

        validate:
            Validates that the value is a non-empty string.

    """

    @staticmethod
    def validate_type(value, param_name: str | None = None) -> None:
        """Validates that the value is a string.

        Args:
            value: The value to validate.
            param_name: Optional name of the parameter being validated.

        Raises:
            TypeError: If the value is not a string.

        Example:
            StringValidator.validate_type("filename.pdf", "file_name")
        """
        if not isinstance(value, str):
            if param_name:
                raise TypeError(f"Invalid {param_name}: value must be a string.")
            raise TypeError("Value must be a string.")

    @staticmethod
    def validate_not_empty(value: str, param_name: str | None = None) -> None:
        """Validates that the string is not empty.

        Note:
            This method does NOT check the type of the value. It assumes the input is
            already a string.
            If you need to validate both type and non-empty, use `validate()` instead.

        Args:
            value (str): The value to validate.
            param_name: Optional name of the parameter being
                validated.

        Raises:
            ValueError: If the value is an empty string.

        Example:
            StringValidator.validate_not_empty("filename.pdf", "file_name")
        """
        if value == "":
            if param_name:
                raise ValueError(
                    f"Invalid {param_name}: value must not be an empty string."
                )
            raise ValueError("Value must not be an empty string.")

    @staticmethod
    def validate(value, param_name: str | None = None) -> None:
        """Validates that the value is a non-empty string.

        Args:
            value: The value to validate.
            param_name: Optional name of the parameter being validated.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is an empty string.

        Example:
            StringValidator.validate("filename.pdf", "file_name")
        """
        StringValidator.validate_type(value, param_name)
        StringValidator.validate_not_empty(value, param_name)
