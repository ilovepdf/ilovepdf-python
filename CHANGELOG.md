# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-24

### Added

- **PdfMarkdownTask** - PDF to Markdown conversion.
- **SummarizeTask** - Content summarization.
- **TranslateTask** - Content translation.
- **SmartSplitTask** - Intelligent PDF splitting.
- **FormsDetectTask** - Form detection.
- Magic byte validation for file type checking in integration tests.

### Fixed

- Authentication now uses locally signed JWT instead of the `/auth` endpoint.
- File tracking in `EditPdfTask` element methods.

### Changed

- Centralized version definition in `ilovepdf/__init__.py` and read it from `pyproject.toml`.

### Updated

- API documentation URLs in sample scripts.

## [1.0.0] - 2026-04-01

Initial stable release.

### Added

- **CompressTask** - PDF compression.
- **EditPdfTask** - PDF editing.
- **ExtractTask** - Content extraction.
- **HtmlToPdfTask** - HTML to PDF conversion.
- **ImagePdfTask** - Image to PDF conversion.
- **MergeTask** - PDF merging.
- **OfficePdfTask** - Office to PDF conversion.
- **PageNumbersTask** - Page number addition.
- **PdfOcrTask** - Optical character recognition (OCR).
- **PdfToJpgTask** - PDF to JPG conversion.
- **PdfToPdfATask** - PDF/A conversion.
- **ProtectTask** - PDF protection.
- **RepairTask** - PDF repair.
- **RotateTask** - Page rotation.
- **SignTask** - Digital signing.
- **SplitTask** - PDF splitting.
- **UnlockTask** - PDF unlocking.
- **ValidatePdfATask** - PDF/A validation.
- **WatermarkTask** - Watermark addition.

[1.1.0]: https://github.com/ilovepdf/ilovepdf-python/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ilovepdf/ilovepdf-python/commit/4129c6be41c4
