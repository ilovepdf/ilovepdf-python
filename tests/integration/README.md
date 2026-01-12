# Integration Tests

This directory contains integration tests for the iLovePDF Python library.

Integration tests validate the interaction between modules and the iLovePDF API, ensuring workflows and external communications function as expected.

**Note:** Integration tests require internet access and valid iLovePDF API credentials.

For general requirements, project structure, and usage examples, see [tests/README.md](../README.md).

---

## Test Files Summary

**Note:** The `files_samples` directory contains input files (PDFs, images, etc.) used for automated tests.
For usage examples and scripts, see the [samples](../../samples/README.md) folder in the project root.

**Example input file:**
A typical input file for integration tests might be `sample.pdf` (PDF format) placed in `integration/files_samples/`.
Make sure your test scripts reference the correct file name and path.

| File Name                           | Description                                                                                   |
|--------------------------------------|----------------------------------------------------------------------------------------------|
| test_00_auth_integration.py          | Tests authentication, credential configuration, token retrieval, and error handling.          |
| test_01_upload_files_integration.py  | Tests file upload flow, large PDF upload, and download verification.                         |
| test_compress_task_integration.py    | Tests CompressTask integration, compression levels, error handling, and compress-download workflow. |
| test_protect_task_integration.py     | Tests ProtectTask integration, password setting, execution, and protected PDF download.       |
| test_sign_basic_task_integration.py  | Tests SignTask integration, signature creation, signer assignment, execution, and result validation. |
| test_split_task_integration.py       | Tests SplitTask integration, splitting by ranges, fixed range, page removal, and max filesize per part. |
| test_unlock_task_integration.py      | Tests UnlockTask integration, password-protected file handling, execution, and unlocked PDF download. |
| test_merge_task_integration.py       | Tests MergeTask integration, multiple PDF merging, execution, and merged PDF download.        |
| test_rotate_task_integration.py      | Tests RotateTask integration, rotation settings, execution, and rotated PDF download.         |
| test_office_pdf_task_integration.py  | Tests OfficePdfTask integration, Office file conversion, execution, and PDF download.         |
| test_pdfocr_task_integration.py      | Tests PdfOcrTask integration, OCR language settings, scanned PDF handling, execution, and result download. |
| test_repair_task_integration.py      | Tests RepairTask integration, corrupted PDF handling, execution, and repaired PDF download.   |
| test_imagepdf_task_integration.py    | Tests ImagePdfTask integration, image-to-PDF conversion using the API.                       |
| test_pdf_to_pdfa_task_integration.py | Tests PdfToPdfATask integration, PDF/A conformance, downgrade options, execution, and PDF/A download. |
| test_extract_task_integration.py     | Tests ExtractTask integration, extraction parameters, execution, and extracted text download. |

_Add new entries to the table above as more integration tests are added._

---

## How to Run Integration Tests

Before running the tests, set the following environment variables with your credentials and sample files path.

**Note:**
Set the environment variable `FOLDER_SAMPLE_PATH` to `"tests/integration/files_samples"` as the default value, regardless of your working directory.
This ensures consistency and avoids confusion.

```bash
export ILOVEPDF_PUBLIC_KEY="your_project_public_key"
export ILOVEPDF_SECRET_KEY="your_project_secret_key"
export FOLDER_SAMPLE_PATH="tests/integration/files_samples"
pytest tests/integration
```

---

## Contributing

- Place new integration test files in this directory.
- Add a brief description to the summary table above.
- Use sample files from `files_samples` and valid API credentials.
- Follow project conventions for naming and documentation.
- Update this README to reflect new tests and instructions.

---

## Links

- [Main README](../../README.md)
- [Unit Tests README](../unit/README.md)
- [Samples README](../../samples/README.md)
- [Official iLovePDF API Documentation](https://developer.ilovepdf.com/docs)

---
