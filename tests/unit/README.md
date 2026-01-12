# Unit Tests

This directory contains unit tests for the iLovePDF Python library.

Unit tests verify the functionality of individual modules and classes in isolation, ensuring correctness and robustness without relying on external services.

For general requirements, project structure, troubleshooting, and usage examples, see [tests/README.md](../README.md).

## Naming Conventions and Dependencies

- All unit test files should be named using the pattern `test_<feature>.py`.
- Test functions and classes should be prefixed with `test_`.
- Unit tests use [pytest](https://docs.pytest.org/) and may use Python's `unittest.mock` for isolation.
- If additional dependencies are required, list them in the test file or in the main requirements.

## Test Files Summary

| File Name                    | Description                                                                                      |
|------------------------------|--------------------------------------------------------------------------------------------------|
| test_ilovepdf.py             | Tests the `Ilovepdf` class: authentication, credential management, token caching, error handling.|
| test_file.py                 | Tests the `File` class: initialization, rotation, password management, file options, PDF page sanitization, form handling.|
| test_upload_files.py         | Tests file upload functionality in `Task` and `File` classes: task creation, file size validation, error handling, multiple uploads.|
| test_ilovepdf_auth_manager.py| Tests the `IlovepdfAuthManager` class: authentication and credentials management using the main class as backend.|
| test_compress_task.py        | Tests the `CompressTask` class: PDF compression functionality and compression level management.   |
| test_split_task.py           | Tests the `SplitTask` class: PDF splitting functionality and split mode management.              |
| test_unlock_task.py          | Tests the `UnlockTask` class: PDF unlocking functionality and password removal process.          |
| test_protect_task.py         | Tests the `ProtectTask` class: PDF protection functionality and password setting process.        |
| test_repair_task.py          | Tests the `RepairTask` class: PDF repair functionality and error recovery process.               |
| test_merge_task.py           | Tests the `MergeTask` class: PDF merging functionality and file combination process.             |
| test_office_pdf_task.py      | Tests the `OfficePdfTask` class: Office to PDF conversion, file extension validation, single-file enforcement.|
| test_pdfocr_task.py         | Tests the `PdfOcrTask` class: OCR language management, file addition, task execution.            |
| test_imagepdf_task.py        | Tests the `ImagePdfTask` class: image-to-PDF conversion, orientation, margin, page size, merge options.|
| test_rotate_task.py          | Tests the `RotateTask` class: PDF page rotation, file addition, task execution.                  |
| test_pdftopdfa_task.py       | Tests the `PdfToPdfATask` class: PDF/A conformance, downgrade options, parameter validation.     |
| test_extract_task.py         | Tests the `ExtractTask` class: text extraction from PDF files and detailed extraction options.   |
| test_watermark_task.py       | Tests the `WatermarkTask` class: watermark mode, text/image parameters, position, font, transparency, layer, validation logic.|

_Add new entries to the table above as more unit tests are added._

## Links

- [Main README](../../README.md)
- [Integration Tests README](../integration/README.md)
- [Samples README](../../samples/README.md)
- [Official iLovePDF API Documentation](https://developer.ilovepdf.com/docs)

## How to Run Unit Tests

To execute all unit tests in this directory, run:

```bash
pytest tests/unit
```

You can also run a specific test file:

```bash
pytest tests/unit/test_compress_task.py
```
