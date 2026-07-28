# ilovepdf Core Library

This folder contains the core Python source code for interacting with the iLovePDF API. All main classes, utilities, and logic for handling PDF processing tasks (such as compressing, merging, splitting, converting, protecting, OCR, signing, and more) are implemented here.

## Structure

- Each module is focused on a specific task or functionality.
- Shared utilities and base classes are organized for reuse and clarity.
- All public classes and methods include type annotations and module-level docstrings.

### Main Task Modules

| Module                     | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| `compress_task.py`         | Compress PDF files to reduce file size.                          |
| `extract_task.py`          | Extract images or text from PDF files.                           |
| `forms_detect_task.py`      | Detect form fields in PDF documents.                            |
| `htmltopdf_task.py`        | Convert HTML documents to PDF.                                   |
| `imagepdf_task.py`         | Convert images to PDF format.                                    |
| `merge_task.py`            | Merge multiple PDF files into a single PDF.                      |
| `office_pdf_task.py`       | Convert Office documents (Word, Excel, PowerPoint) to PDF.       |
| `pdfmarkdown_task.py`     | Convert PDF files to Markdown format.                            |
| `pdfocr_task.py`           | Perform OCR (Optical Character Recognition) on PDF files.        |
| `pdftojpg_task.py`         | Convert PDF files to JPG images (pages or extract mode).         |
| `pdftopdfa_task.py`        | Convert PDF files to PDF/A archival format.                      |
| `protect_task.py`          | Add password protection and permissions to PDF files.            |
| `repair_task.py`           | Repair corrupted or damaged PDF files.                           |
| `rotate_task.py`           | Rotate PDF pages by specified angles.                            |
| `sign_task.py`             | Digitally sign PDF documents.                                    |
| `smart_split_task.py`      | AI-powered smart PDF splitting based on content analysis.        |
| `summarize_task.py`        | AI-powered PDF summarization in multiple languages and formats.   |
| `translate_task.py`         | AI-powered PDF translation to multiple target languages.           |
| `split_task.py`            | Split PDF files into separate documents.                         |
| `unlock_task.py`           | Remove password protection from PDF files.                       |
| `watermark_task.py`        | Add text or image watermarks to PDFs.                            |
| `pagenumbers_task.py`      | Add page numbers to PDFs with customizable appearance.           |
| `editpdf_task.py`          | Add and position text, image, SVG, or bottom elements on PDFs.   |
| `validate_pdfa_task.py`    | Validate PDF/A compliance of PDF files (no conversion).          |

#### Other Modules

- `helpers.py`: Helper functions and type definitions (literals, options).
- `file.py`: File handling utilities for tasks.
- `abstract_task_element.py`: AbstractTaskElement base class for task elements.
- `ilovepdf_api.py`: Core API communication logic.
- `task.py`: Base class for all tasks.
- `exceptions/`: Custom exception classes for error handling.
- `validators/`: Input validation utilities for robust parameter checking.
- `sign/`: Utilities and helpers for digital signature workflows.

## Development Guidelines

- Keep the code modular and well-documented.
- Ensure all new modules and classes include appropriate docstrings (Google style, in English).
- Any file ending with `*_task.py` must have corresponding unit and integration tests, as well as a sample script
- Use type hints for all public methods and properties.
- Follow PEP 8 and project-specific naming conventions.
- Use the provided validators for input validation in tasks and models.

## Related Documentation

- [Project Overview](../README.md)
- [Samples and Usage](../samples/README.md)
- [Testing](../tests/README.md)
- [Docker and Environment Setup](../.docker/README.md)
- [Installation](../INSTALL.md) - All install options
- [Development](../DEVELOPMENT.md) - Contributing & setup

For the official API documentation, visit: [iLovePDF API Docs](https://developer.ilovepdf.com/docs)
