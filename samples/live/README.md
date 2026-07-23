# Live Samples (`samples/live/`)

This folder contains **live/manual test scripts** for the iLovePDF Python library. These scripts execute real workflows against the iLovePDF API using real credentials and files.

All live scripts must remain minimal:

- Keep comments and docstrings short.
- Mirror the structure of existing live scripts (for example, `pdftojpg_basic.py`).
- Demonstrate only the essential workflow for manual validation.

---

## Purpose

- **Manual validation:** Verify real API integrations end to end.
- **Debugging:** Reproduce issues that automated tests might miss.
- **Demonstration:** Showcase real responses and outputs to collaborators.

> Live scripts are not intended for onboarding or documentation—they are purely for manual checks.

---

## Important Notes

- **No automation:** Do not run these scripts in CI/CD.
- **Real credentials required:** Provide valid API keys and real sample files.
- **Never commit secrets:** Credentials must come from environment variables or local config only.
- **API usage:** Running these scripts consumes API quota and may incur costs.

---

## How to Use

1. **Environment setup**

   - Export `ILOVEPDF_PUBLIC_KEY` and `ILOVEPDF_SECRET_KEY`, or configure a `.env` file.
   - Ensure required sample files exist (check each script for paths).
   - Create an `output_live` directory if it does not exist:

     ```bash
     mkdir -p output_live
     ```

2. **Install dependencies**

   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run a live script**

   ```bash
   python samples/live/<script_name>.py
   ```

4. **Check results**

   - Inspect console output for API responses.
   - Downloaded files are typically saved under `output_live/`.

---

## Folder Policy

- Keep scripts synchronized with the latest SDK behavior.
- Do not add confidential client data.
- Document any special requirements inside the script or in this README.

---

## When to Use Live Samples

- Validating new features directly against the production API.
- Investigating integration bugs from support cases.
- Demonstrating workflows to stakeholders with real data.

---

## Available Live Samples

### Compression

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `compress_basic.py`     | Compresses `sample.pdf` using `CompressTask` and downloads the result.              |
| `compress_advanced.py`  | Advanced compression of multiple PDFs with custom compression levels.               |

### Splitting

| Script                      | Description                                                                     |
| --------------------------- | ------------------------------------------------------------------------------- |
| `split_basic.py`            | Splits `sample.pdf` by ranges (`2-4,6-8`) and downloads a ZIP with results.    |
| `split_advanced.py`         | Advanced PDF splitting with custom ranges and options.                          |
| `split_advanced_merge.py`   | Splits `sample.pdf` by ranges and merges results into a single PDF.            |

### Conversion

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `office_pdf_basic.py`   | Converts `sample_word.docx` to PDF using `OfficePdfTask`.                          |
| `html_to_pdf_basic.py`  | Converts a URL (`https://example.com`) to PDF using `HtmlToPdfTask`.               |
| `imagepdf_basic.py`     | Converts images (JPG, PNG) to a merged PDF using `ImagePdfTask`.                   |
| `pdftojpg_basic.py`     | Converts `sample.pdf` into JPG pages using `PdfToJpgTask`, downloads a ZIP result. |
| `pdftopdfa_basic.py`    | Converts `sample.pdf` to PDF/A format using `PdfToPdfATask`.                       |
| `pdftopdfa_advanced.py` | Converts multiple PDFs to PDF/A format, downloads result as ZIP.                   |
| `pdfocr_basic.py`       | Performs OCR on `sample.pdf` with Spanish language using `PdfOcrTask`.              |
| `extract_basic.py`      | Extracts text from `sample.pdf` using `ExtractTask` (detailed mode).               |

### Editing

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `editpdf_basic.py`      | Places a styled text element on `sample-1-2.pdf` using `EditPdfTask`.              |
| `editpdf_advanced.py`   | Stacks text, image, and SVG elements on `sample-1-2.pdf` with `EditPdfTask`.       |

### Merging

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `merge_basic.py`        | Merges two PDFs into a single file using `MergeTask`.                              |

### Rotation

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `rotate_basic.py`       | Rotates `sample.pdf` pages by 90 degrees using `RotateTask`.                       |

### Watermarking

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `watermark_basic.py`    | Adds a text watermark to `sample.pdf` using `WatermarkTask`.                       |
| `watermark_advanced.py` | Advanced watermarking with custom text options and positioning.                     |

### Page Numbers

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `pagenumbers_basic.py`  | Adds page numbers to `sample.pdf` with custom position, format, font, and color.   |

### Signing

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `sign_basic.py`         | Basic digital signature workflow on `sample.pdf` using `SignTask`.                  |
| `sign_advanced.py`      | Advanced signature workflow with multiple signers using `SignTask`.                 |

### Validation

| Script                      | Description                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------- |
| `validate_pdfa_basic.py`    | Validates PDF/A compliance of `sample.pdf` using `ValidatePdfATask`.               |

### Protection & Unlocking

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `protect_basic.py`      | Adds password protection to `sample.pdf` using `ProtectTask`.                      |
| `unlock_basic.py`       | Removes password protection from a PDF using `UnlockTask`.                         |

### Repair

| Script                  | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `repair_basic.py`       | Repairs `sample.pdf` using `RepairTask` and downloads the result.                  |

---

For standard (non-live) examples, refer to the parent [`samples/`](../README.md) directory. For automated coverage, see the [`tests/`](../../tests/) folder.

---

## Related Documentation

- [Project Overview](../../README.md)
- [Samples Overview](../README.md)
- [Core Library](../../ilovepdf/README.md)
- [Testing](../../tests/README.md)
- [Docker and Environment Setup](../../.docker/README.md)
