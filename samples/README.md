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

   You can copy `.env.example` to `.env` and fill in your credentials.

2. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run the script**
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
- `smart_split_basic.py`: AI-powered smart split based on content analysis.

**Conversion**
- `office_pdf_basic.py`: Convert an Office document (Excel, Word, PowerPoint) to PDF.
- `html_to_pdf_basic.py`: Convert an HTML document to PDF.
- `imagepdf_basic.py`: Convert images to PDF.
- `pdftojpg_basic.py`: Convert a PDF file to JPG images (each page as a JPG or extract images).
- `pdftopdfa_basic.py`: Convert a PDF to PDF/A.
- `pdftopdfa_advanced.py`: Advanced PDF/A conversion options.
- `validate_pdfa_basic.py`: Validate if a PDF is PDF/A compliant (no conversion).
- `pdfocr_basic.py`: Perform OCR on a PDF with language configuration.
- `extract_basic.py`: Extract text from a PDF.

**Editing**
- `editpdf_basic.py`: Basic EditPdfTask example that places a single text element on
  the first page and downloads the updated PDF.
- `editpdf_advanced.py`: Advanced EditPdfTask workflow combining text, image, and SVG
  elements with custom styling and stacking order.

**Merging**
- `merge_basic.py`: Merge multiple PDF files into a single PDF.

**Rotation**
- `rotate_basic.py`: Rotate pages in a PDF file.

**Watermarking**
- `watermark_basic.py`: Add a watermark (text or image) to a PDF.
- `watermark_advanced.py`: Advanced watermarking with custom options.

**Page Numbers**
- `pagenumbers_basic.py`: Add page numbers to a PDF with customizable position, format, and appearance.

**Signing**
- `sign_basic.py`: Basic digital signature workflow.
- `sign_advanced.py`: Advanced digital signature workflow with multiple receivers/elements.

**Protection**
- `protect_basic.py`: Add password protection to a PDF file.

**Unlocking & Repair**
- `unlock_basic.py`: Unlock a password-protected PDF.
- `repair_basic.py`: Repair a corrupted PDF.

---

## Live Samples (`samples/live/`)

The `live/` subfolder contains scripts designed for **manual, real-world testing** of the library against the actual iLovePDF API. These scripts:

- Require valid API credentials and real files.
- Are not intended for automated testing or CI/CD.
- Should be used for debugging, advanced validation, or when you need to verify the library in a real environment.
- Must never include sensitive data or credentials directly in the code.

For the full list of available live scripts, setup instructions, and usage details, see [`samples/live/README.md`](live/README.md).

---

## More Information

- For full project documentation and API usage, see the [main README](../README.md).
- For detailed API reference, visit the [official iLovePDF API docs](https://developer.ilovepdf.com/docs).
