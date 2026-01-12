"""Provides a DateValidator class for validating date strings in allowed formats.

Supports validation for multiple date formats commonly used in ilovepdf tasks.
"""

from datetime import datetime
from typing import List, Optional

DATE_FORMATS: List[str] = [
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d.%m.%Y",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%m-%d-%Y",
    "%m/%d/%Y",
    "%m.%d.%Y",
]


class DateValidator:
    """Validator for date strings with multiple allowed formats."""

    @staticmethod
    def validate_format(date_str: str, param_name: Optional[str] = None) -> None:
        """
        Validates that the input string matches one of the allowed date formats.

        Args:
            date_str (str): The date string to validate.
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            ValueError: If the date string does not match any allowed format.
        """
        if not isinstance(date_str, str):
            name = f" for {param_name}" if param_name else ""
            raise TypeError(f"Value{name} must be a string.")

        for fmt in DATE_FORMATS:
            try:
                datetime.strptime(date_str, fmt)
                return
            except ValueError:
                continue

        name = f" for {param_name}" if param_name else ""
        raise ValueError(
            f"Invalid date format{name}: must match one of {DATE_FORMATS}."
        )

    @staticmethod
    def validate_in_range(
        date_str: str,
        min_date: Optional[str] = None,
        max_date: Optional[str] = None,
        param_name: Optional[str] = None,
    ) -> None:
        """
        Validates that the date string is within the specified range.

        Args:
            date_str (str): The date string to validate.
            min_date (Optional[str]): Minimum allowed date (same format as date_str).
            max_date (Optional[str]): Maximum allowed date (same format as date_str).
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            ValueError: If the date string is not in a valid format or out of range.
        """
        # Validate format first
        for fmt in DATE_FORMATS:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            name = f" for {param_name}" if param_name else ""
            raise ValueError(
                f"Invalid date format{name}: must match one of {DATE_FORMATS}."
            )

        if min_date:
            min_obj = DateValidator._parse_date(min_date)
            if date_obj < min_obj:
                name = f" for {param_name}" if param_name else ""
                raise ValueError(f"Date{name} must be on or after {min_date}.")
        if max_date:
            max_obj = DateValidator._parse_date(max_date)
            if date_obj > max_obj:
                name = f" for {param_name}" if param_name else ""
                raise ValueError(f"Date{name} must be on or before {max_date}.")

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """
        Parses a date string using allowed formats.

        Args:
            date_str (str): The date string to parse.

        Returns:
            datetime: The parsed datetime object.

        Raises:
            ValueError: If the date string does not match any allowed format.
        """
        for fmt in DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: must match one of {DATE_FORMATS}.")
