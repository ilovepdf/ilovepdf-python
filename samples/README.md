# Samples

This directory contains example scripts demonstrating how to use the iLovePDF Python library to interact with the iLovePDF API.

There are two types of samples:
- **Standard samples:** Simple, self-contained examples for each main task of the library.
- **Live samples (`samples/live/`):** Manual test scripts that run real workflows against the API using actual files and credentials. These scripts require special configuration and should not be run in automated environments or CI/CD.

Each script illustrates a specific task, such as compressing, splitting, converting, merging PDFs, and more. Examples are designed to be simple, self-contained, and easy to adapt for your own use cases.

---

## Structure

- Each script focuses on a single use case or workflow.
- Scripts are grouped by task type (compression, conversion, splitting, etc.).
- All scripts include a brief description and helpful comments at the top.
- Examples follow the project documentation and style guidelines.
- The `live/` subfolder contains scripts for real manual testing (see below).

---

## How to Run the Examples

Before running any example script:

1. **Set environment variables**  
   Make sure you have set the required environment variables for authentication:
   - `ILOVEPDF_PUBLIC_KEY`
   - `ILOVEPDF_SECRET_KEY`
   - Optionally, `FOLDER_SAMPLE_PATH` for sample files

   You can copy `.docker/.env.sample` to `.docker/.env` and fill in your credentials.

2. **Install dependencies**  
   Install the library and its dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run the script**  
   Execute any example script with:
   ```bash
   python <script_name>.py
   ```

---

## List of Example Scripts

**Compression**
- `compress_basic.py`: Basic PDF compression example.
- `compress_advanced.py`: Advanced compression workflow with custom parameters.

**Splitting**
- `split_basic.py`: Split a PDF into separate pages.
- `split_advanced.py`: Advanced splitting with custom ranges or split modes.
- `split_advanced_merge.py`: Split a PDF and then merge selected pages.

**Conversion**
- `office_pdf_basic.py`: Convert an Office document (Excel, Word, PowerPoint) to PDF.
- `imagepdf_basic.py`: Convert images to PDF.
- `pdftopdfa_basic.py`: Convert a PDF to PDF/A.
- `pdftopdfa_advanced.py`: Advanced PDF/A conversion options.
- `pdfocr_basic.py`: Perform OCR on a PDF with language configuration.
- `extract_basic.py`: Extract text from a PDF.

**Rotation**
- `rotate_basic.py`: Rotate pages in a PDF file.

**Watermarking**
- `watermark_basic.py`: Add a watermark (text or image) to a PDF.
- `watermark_advanced.py`: Advanced watermarking with custom options.

**Signing**
- `sign_basic.py`: Basic digital signature workflow.
- `sign_advanced.py`: Advanced digital signature workflow with multiple receivers/elements.

**Unlocking & Repair**
- `unlock_basic.py`: Unlock a password-protected PDF.
- `repair_basic.py`: Repair a corrupted PDF.

_Note: All scripts conform to AGENT.md and core conventions. If a sample for a Task is missing, please contribute to maintain coverage and style compliance._

---

## Live Samples (`samples/live/`)

The `live/` subfolder contains scripts designed for **manual, real-world testing** of the library against the actual iLovePDF API. These scripts:

- Require valid API credentials and real files.
- Are not intended for automated testing or CI/CD.
- Should be used for debugging, advanced validation, or when you need to verify the library in a real environment.
- Must never include sensitive data or credentials directly in the code.

**How to use:**
1. Configure your environment variables or `.env` file with real API keys and sample files.
2. Run the scripts manually as needed to validate real API flows.
3. Review the `samples/live/README.md` for more details and usage instructions.

---

---

## More Information

- For full project documentation and API usage, see the [main README](../README.md).
- For detailed API reference, visit the [official iLovePDF API docs](https://developer.ilovepdf.com/docs).

---
