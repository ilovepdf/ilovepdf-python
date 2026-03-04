# Integration Tests

This folder contains integration tests for the iLovePDF Python library. Integration tests are designed to verify the correct interaction between the library and the iLovePDF API, as well as to validate end-to-end workflows involving real API calls and file operations.

## Structure

- Each test file targets a specific feature or workflow (e.g., PDF compression, merging, conversion, OCR).
- Tests may require valid API credentials and sample PDF/image files.

## Running Integration Tests

1. Ensure you have a valid `.env` file in the `.docker/` directory with the following variables set:
   - `ILOVEPDF_PUBLIC_KEY`
   - `ILOVEPDF_SECRET_KEY`
   - `FOLDER_SAMPLE_PATH` (default: `tests/integration/files_samples`)

2. Run the tests using your preferred test runner (e.g., `pytest`):

```bash
pytest tests/integration
```

## Test Files

| File Name                                   | Description                                                                                  |
|---------------------------------------------|----------------------------------------------------------------------------------------------|
| test_integration_00_auth.py                 | Integration tests for authentication and API key validation.                                 |
| test_integration_01_upload_files.py         | Integration tests for uploading files to the API.                                            |
| test_integration_compress_task.py           | Integration tests for CompressTask, covering full workflow: adding files, setting compression parameters, executing, and downloading results. |
| test_integration_extract_task.py            | Integration tests for ExtractTask, covering extraction of text or images from PDFs.           |
| test_integration_htmltopdf_task.py          | Integration tests for HtmlToPdfTask, converting HTML to PDF and validating options.           |
| test_integration_imagepdf_task.py           | Integration tests for ImagePdfTask, converting images to PDF and merging.                     |
| test_integration_merge_task.py              | Integration tests for MergeTask, merging multiple PDF files.                                  |
| test_integration_office_pdf_task.py         | Integration tests for OfficePdfTask, converting Office files to PDF.                          |
| test_integration_pdfocr_task.py             | Integration tests for PdfOcrTask, performing OCR on scanned PDFs.                             |
| test_integration_pdftojpg_task.py           | Integration tests for PdfToJpgTask, converting PDF files to JPG images in 'pages' and 'extract' modes. |
| test_integration_pdftopdfa_task.py           | Integration tests for PdfToPdfATask, converting PDFs to PDF/A format.                         |
| test_integration_validate_pdfa_task.py       | Integration tests for ValidatePdfATask, validating PDF/A compliance of PDF files.             |
| test_integration_protect_task.py             | Integration tests for ProtectTask, adding password protection to PDFs.                        |
| test_integration_repair_task.py             | Integration tests for RepairTask, repairing corrupted PDFs.                                   |
| test_integration_rotate_task.py             | Integration tests for RotateTask, rotating PDF pages.                                         |
| test_integration_sign_basic_task.py         | Integration tests for SignTask, digital signature workflows.                                  |
| test_integration_split_task.py              | Integration tests for SplitTask, splitting PDFs by range, pages, or size.                     |
| test_integration_unlock_task.py             | Integration tests for UnlockTask, removing password protection from PDFs.                     |
| test_integration_watermark_task.py          | Integration tests for WatermarkTask, adding text or image watermarks to PDFs.                 |
| test_integration_pagenumbers_task.py        | Integration tests for PageNumbersTask, adding page numbers to PDFs with customizable appearance and format. |
| test_integration_editpdf_task.py            | Integration tests for EditPdfTask, covering text, image, and SVG elements plus execute/download workflows. |

Update this table as new integration tests are added.

## Notes

- Integration tests may consume API quota and require internet access.
- Sensitive data such as API keys should never be committed to the repository.
