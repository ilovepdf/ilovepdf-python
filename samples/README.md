# Example Scripts

## Purpose

This directory contains example scripts demonstrating common use cases for the iLovePDF Python library. These scripts are designed to help users and contributors understand how to automate PDF tasks using the library's main features.

---

## Requirements

- Python >= 3.9
- [iLovePDF API credentials](https://developer.ilovepdf.com/user/projects)
- All dependencies installed as described in the [main README](../README.md)

---

**Script Naming Convention:**
Sample scripts should be named using the pattern `<task>_<usage>.py` (e.g., `compress_basic.py`, `split_advanced.py`) to clearly indicate the Task and usage scenario.

**Input Files:**
Most scripts require input PDF or image files. You may use your own files or those provided in the `tests/integration/files_samples` directory for testing purposes.

## Script Files Summary

| Script Name               | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| compress_basic.py         | Compress a PDF file using the `CompressTask` class with basic usage (add file, execute, download).|
| compress_advanced.py      | Advanced compression options: file rotation, compression level, custom output filename.           |
| split_basic.py            | Split a PDF into separate pages using the `SplitTask` class.                                      |
| split_advanced.py         | Advanced splitting: custom ranges or split modes with the `SplitTask` class.                      |
| split_advanced_merge.py   | Split a PDF and then merge selected pages, combining `SplitTask` and merge functionality.         |
| office_pdf_basic.py       | Convert an Office document (Excel, Word, PowerPoint) to PDF using the `OfficePdfTask` class.      |
| rotate_basic.py           | Rotate pages in a PDF file using the `RotateTask` class.                                          |
| imagepdf_basic.py         | Convert images to a PDF file using the `ImagePdfTask` class.                                      |
| pdftopdfa_basic.py      | Convert a PDF to PDF/A format using the `PdfToPdfATask` class.                                    |
| pdftopdfa_advanced.py   | Advanced PDF/A conversion options using the `PdfToPdfATask` class.                                |
| pdfocr_basic.py           | Perform OCR on a PDF file using the `PdfOcrTask` class, including language configuration.         |
| extract_basic.py          | Extract text from a PDF file using the `ExtractTask` class.                                       |
| watermark_basic.py        | Add a watermark (text or image) to a PDF file using the `WatermarkTask` class.                    |
| watermark_advanced.py     | Advanced watermark options: position, font, transparency, layer.                                  |
| sign_basic.py             | Create a basic digital signature workflow using the `SignTask` class.                             |
| sign_advanced.py          | Advanced digital signature workflows with multiple elements and receivers using the `SignTask` class.|
| unlock_basic.py           | Unlock a password-protected PDF using the `UnlockTask` class.                       |

_Note: If a sample script for a Task is missing, please contribute one to ensure full coverage and compliance with project rules._

---

## How to Use the Examples

1. Ensure you have installed all required dependencies as described in the [main README](../README.md).
2. Set your iLovePDF API credentials in each script before running:
   - `ILOVEPDF_PUBLIC_KEY`
   - `ILOVEPDF_SECRET_KEY`
3. Run any example script from the command line, for example:
   ```bash
   python compress_basic.py
   ```
4. Review the module-level docstring at the top of each script for usage details and configurable parameters.

---

## Adding New Example Scripts

- Place new scripts in this directory.
- Add a brief description to the summary table above.
- Ensure each script includes a module-level docstring describing its purpose, usage, and configurable parameters.
- Update this README to describe the new script and its purpose.

---

## Troubleshooting

- **Missing API credentials:** Ensure you have set your public and secret keys as environment variables or directly in the script.
- **Dependency errors:** Install all required packages using `pip install -r requirements.txt` or as described in the main README.
- **File not found:** Verify the sample files exist and paths are correct.

---

## FAQ

**Q: Where do I get my iLovePDF API credentials?**
A: Register and create a project at [iLovePDF Developer Portal](https://developer.ilovepdf.com/user/projects).

**Q: Can I run these scripts without an internet connection?**
A: No, all scripts require access to the iLovePDF API.

**Q: How do I contribute a new example?**
A: Add your script to this folder, update the summary table, and ensure it follows the documentation standards.

---

## Links

- [Main README](../README.md)
- [Official iLovePDF API Documentation](https://developer.ilovepdf.com/docs)
- [Contribution Guide](../CONTRIBUTING.md)
