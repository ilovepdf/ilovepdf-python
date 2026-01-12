# Unit Tests

This folder contains unit tests for the core modules and classes of the `ilovepdf` Python library.

## Purpose

Unit tests are designed to verify the correctness of individual functions, classes, and methods in isolation, without requiring access to external services or the iLovePDF API. These tests help ensure that the internal logic of the library works as expected.

## Structure

- Each test file targets a specific module or class in the `ilovepdf/` directory.
- Test files are named according to the module or feature they cover, typically following the pattern: `test_<module>.py`.
- Tests are organized by functionality, ensuring focused validation and comprehensive coverage.

## Test Files

### Core API and Authentication

- `test_ilovepdf.py` - Ilovepdf core class and API initialization
- `test_ilovepdf_auth_manager.py` - Authentication manager and credential handling
- `test_error_router.py` - ErrorRouter error handling and exception routing

### Task Classes

- `test_task.py` - Base Task class with file management and validation
- `test_task_methods.py` - Task class methods (start, upload_file, download, execute, get_status)
- `test_compress_task.py` - CompressTask validation and compression level settings
- `test_extract_task.py` - ExtractTask extraction parameters and detailed mode
- `test_htmltopdf_task.py` - HtmlToPdfTask HTML-to-PDF conversion parameters
- `test_imagepdf_task.py` - ImagePdfTask image-to-PDF conversion and parameter validation
- `test_merge_task.py` - MergeTask basic instantiation and payload
- `test_office_pdf_task.py` - OfficePdfTask office file extension validation and single-file enforcement
- `test_pdfocr_task.py` - PdfOcrTask and OcrFile OCR language configuration
- `test_pdftopdfa_task.py` - PdfToPdfATask PDF/A conformance and downgrade options
- `test_protect_task.py` - ProtectTask password protection and payload validation
- `test_repair_task.py` - RepairTask single-file enforcement and initialization
- `test_rotate_task.py` - RotateTask rotation angles and validation
- `test_sign_task.py` - SignTask signer and file management, property setters, and full flow
- `test_signer_file.py` - SignerFile file and element management for signature tasks
- `test_sign_signer.py` - Signer signer type, access code, and file association
- `test_split_task.py` - SplitTask split modes, parameter validation, and payload
- `test_unlock_task.py` - UnlockTask basic instantiation and payload
- `test_watermark_task.py` - WatermarkTask watermarking features
- `test_removebackground_task.py` - RemoveBackgroundTask initialization and configuration

### Validators

- `test_bool_validator.py` - BoolValidator strict boolean validation
- `test_choice_validator.py` - Choice validation for restricted value sets
- `test_int_validator.py` - Integer validation with range and option constraints
- `test_string_validator.py` - StringValidator string type and non-empty validation

### Exception Handling

- `test_base_custom_exception.py` - BaseCustomException features and behavior
- `test_process_exception.py` - ProcessException handling
- `test_int_errors.py` - Integer validation error exceptions

### Utilities and Builders

- `test_payload_builder.py` - PayloadBuilder for request payload construction

### Base Infrastructure

- `base_test.py` - Reusable test fixtures and base classes (no direct tests)

## How to Run Unit Tests

Run all unit tests:
```bash
pytest tests/unit -q
```

Run specific test file:
```bash
pytest tests/unit/test_<module>.py -v
```

Run with coverage report:
```bash
pytest tests/unit --cov=ilovepdf --cov-report=term
```

Run specific test class:
```bash
pytest tests/unit/test_<module>.py::TestClassName -v
```

Run tests matching a pattern:
```bash
pytest tests/unit -k "compress" -v
```

## Test Quality Standards

- **Focused Scope**: Each test validates specific functionality relevant to its module
- **Edge Cases**: Important edge cases and error conditions are thoroughly tested
- **Isolation**: Tests use mocking to avoid dependencies on external services
- **Clarity**: Test names clearly describe what is being tested
- **Maintainability**: Organized structure with consistent naming conventions

## Notes

- All new modules and public methods in `ilovepdf/` should have corresponding unit tests here.
- Each test file should start with a module-level docstring describing its purpose.
- Use `AbstractUnitTaskTest` as the base class for task-related unit tests.
- Include the line `# pylint: disable=protected-access` at the top of test files that access protected members.
- When adding new tests, update this README to reflect the changes.

---