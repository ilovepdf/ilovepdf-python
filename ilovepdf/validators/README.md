# Validators Module

## Overview

The `validators` module provides reusable validator classes for validating various parameter types and values used throughout the ilovepdf-python library.

## Validators

### StringValidator

Validates that a value is a string and/or not an empty string.

**Methods:**
- `validate_type(value, param_name)` - Ensure value is a string
- `validate_not_empty(value, param_name)` - Ensure string is not empty
- `validate(value, param_name)` - Ensure value is a string and not empty

**Examples:**
```python
from ilovepdf.validators import StringValidator

# Validate type only
StringValidator.validate_type("filename.pdf", "file_name")  # OK
StringValidator.validate_type(123, "file_name")  # Raises TypeError

# Validate not empty only (assumes input is already a string)
StringValidator.validate_not_empty("filename.pdf", "file_name")  # OK
StringValidator.validate_not_empty("", "file_name")  # Raises ValueError

# Validate both type and not empty
StringValidator.validate("filename.pdf", "file_name")  # OK
StringValidator.validate("", "file_name")  # Raises ValueError
StringValidator.validate(123, "file_name")  # Raises TypeError
```

### IntValidator

Validates integer values with various constraints.

**Methods:**
- `validate_type(value, param_name)` - Ensure value is an integer
- `validate_positive(value, param_name)` - Ensure value is a positive integer (> 0)
- `validate_range(value, min_value, max_value, param_name)` - Ensure value is within range
- `validate_options(value, options, param_name)` - Ensure value is in allowed set

**Example:**
```python
from ilovepdf.validators import IntValidator

# Validate type
IntValidator.validate_type(5)  # OK
IntValidator.validate_type("5")  # Raises NotAnIntError

# Validate positive
IntValidator.validate_positive(10, "width")  # OK
IntValidator.validate_positive(0, "width")  # Raises IntOutOfRangeError

# Validate range
IntValidator.validate_range(50, 1, 100, "quality")  # OK
IntValidator.validate_range(150, 1, 100, "quality")  # Raises IntOutOfRangeError

# Validate options
IntValidator.validate_options(90, {0, 90, 180, 270}, "rotation")  # OK
IntValidator.validate_options(45, {0, 90, 180, 270}, "rotation")  # Raises IntNotInAllowedSetError
```

### FloatValidator

Validates float values with various constraints.

**Methods:**
- `validate_type(value, param_name)` - Ensure value is a float
- `validate_positive(value, param_name)` - Ensure value is a positive float (> 0)
- `validate_range(value, min_value, max_value, param_name)` - Ensure value is within range
- `validate_options(value, options, param_name)` - Ensure value is in allowed set

**Example:**
```python
from ilovepdf.validators import FloatValidator

# Validate type
FloatValidator.validate_type(5.0)  # OK
FloatValidator.validate_type("5.0")  # Raises TypeError

# Validate positive
FloatValidator.validate_positive(10.5, "scale")  # OK
FloatValidator.validate_positive(0.0, "scale")  # Raises FloatOutOfRangeError

# Validate range
FloatValidator.validate_range(0.75, 0.5, 1.0, "quality")  # OK
FloatValidator.validate_range(1.5, 0.5, 1.0, "quality")  # Raises FloatOutOfRangeError

# Validate options
FloatValidator.validate_options(0.5, {0.5, 0.75, 1.0}, "quality")  # OK
FloatValidator.validate_options(0.6, {0.5, 0.75, 1.0}, "quality")  # Raises InvalidChoiceError
```

**Exceptions:**
- `TypeError` - If the value is not a float
- `FloatOutOfRangeError` - If the value is outside the allowed range or not positive
- `InvalidChoiceError` - If the value is not among allowed choices

### DateValidator

Validates date strings against multiple allowed formats and optional range.

**Methods:**
- `validate_format(date_str, param_name)` - Ensure value matches one of the allowed date formats
- `validate_in_range(date_str, min_date, max_date, param_name)` - Ensure value is a valid date and within the specified range

**Example:**
```python
from ilovepdf.validators import DateValidator

# Validate format
DateValidator.validate_format("31-12-2024")  # OK
DateValidator.validate_format("2024/12/31")  # OK
DateValidator.validate_format("31/13/2024")  # Raises ValueError (invalid month)
DateValidator.validate_format("2024-31-12")  # Raises ValueError (invalid format)

# Validate in range
DateValidator.validate_in_range("31-12-2024", min_date="01-01-2024", max_date="31-12-2024")  # OK
DateValidator.validate_in_range("01-01-2023", min_date="01-01-2024", max_date="31-12-2024")  # Raises ValueError (out of range)
```

**Exceptions:**
- `TypeError` - If the value is not a string
- `ValueError` - If the value does not match any allowed format or is out of range

### ChoiceValidator

Validates that values are among a set of allowed choices.

**Methods:**
- `validate(value, allowed, param_name, cls_error)` - Ensure value is in allowed choices

**Parameters:**
- `value` (Any): The value to validate
- `allowed` (Iterable[Any]): Set of allowed values
- `param_name` (str, optional): Parameter name for error messages. Default: "parameter"
- `cls_error` (Type[Exception], optional): Exception class to raise. Default: InvalidChoiceError

**Example:**
```python
from ilovepdf.validators import ChoiceValidator
from ilovepdf.exceptions import InvalidChoiceError

# Validate with default error
ChoiceValidator.validate("jpg", ["jpg", "png", "gif"], "format")  # OK
ChoiceValidator.validate("bmp", ["jpg", "png", "gif"], "format")  # Raises InvalidChoiceError

# Validate with custom error
from ilovepdf.exceptions import IntNotInAllowedSetError

ChoiceValidator.validate(
    90,
    {0, 90, 180, 270},
    "rotation",
    cls_error=IntNotInAllowedSetError
)  # OK or raises IntNotInAllowedSetError
```

## Exceptions

Validators use the following exceptions from `ilovepdf.exceptions`:

- `TypeError` - Raised by StringValidator when a value is not a string, by FloatValidator when a value is not a float, or by DateValidator when a value is not a string
- `ValueError` - Raised by StringValidator when a string is empty, or by DateValidator when a date string is invalid or out of range
- `NotAnIntError` - Raised when a value is not an integer
- `IntOutOfRangeError` - Raised when an integer is outside the allowed range
- `IntNotInAllowedSetError` - Raised when an integer is not in the allowed set
- `FloatOutOfRangeError` - Raised when a float is outside the allowed range or not positive
- `InvalidChoiceError` - Raised when a value is not among allowed choices

## Usage in Tasks

Validators are used internally by task classes to validate parameters:

```python
from ilovepdf.compress_task import CompressTask
from ilovepdf.validators import StringValidator

task = CompressTask(public_key="your_key", secret_key="your_secret")
task.compression_level = "low"  # Uses validators internally

# Example of using StringValidator in a setter
class ExampleTask:
    @property
    def file_name(self) -> str:
        """Gets the file name."""
        return self._file_name

    @file_name.setter
    def file_name(self, value: str):
        """
        Sets the file name.

        Args:
            value (str): Must be a non-empty string.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string.
        """
        StringValidator.validate(value, "file_name")
        self._file_name = value
```



## Performance Considerations

- All validators are implemented as static methods for minimal overhead
- Validators use simple type checking and comparison
- No caching or memoization (validation is lightweight)
- Suitable for frequent validation calls

## Testing

Each validator has comprehensive unit tests in `tests/unit/`:
- `test_string_validator.py` - Tests for StringValidator
- `test_int_validator.py` - Tests for IntValidator
- `test_bool_validator.py` - Tests for BoolValidator
- `test_choice_validator.py` - Tests for ChoiceValidator

Run tests with:
```bash
pytest tests/unit/test_string_validator.py -v
pytest tests/unit/test_int_validator.py -v
pytest tests/unit/test_bool_validator.py -v
pytest tests/unit/test_choice_validator.py -v
```

## See Also

- `ilovepdf/abstract_task_element.py` - AbstractTaskElement base class
- `ilovepdf/exceptions/` - Exception definitions
- `tests/unit/` - Validator tests
