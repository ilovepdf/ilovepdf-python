"""
Handles PDF OCR tasks using the iLovePDF API.

Provides the PdfOcrTask and OcrFile classes to configure and execute optical
character recognition (OCR) on PDF files. Supported languages are documented in
``OCR_LANGUAGE_OPTIONS``.
"""

from typing import Literal

from .file import File
from .task import Task
from .validators import ChoiceValidator

OcrLanguageType = Literal[
    "eng",
    "afr",
    "amh",
    "ara",
    "asm",
    "aze",
    "aze_cyrl",
    "bel",
    "ben",
    "bod",
    "bos",
    "bre",
    "bul",
    "cat",
    "ceb",
    "ces",
    "chi_sim",
    "chi_tra",
    "chr",
    "cos",
    "cym",
    "dan",
    "deu",
    "deu_latf",
    "dzo",
    "ell",
    "enm",
    "epo",
    "equ",
    "est",
    "eus",
    "fao",
    "fas",
    "fil",
    "fin",
    "fra",
    "frm",
    "fry",
    "gla",
    "gle",
    "glg",
    "grc",
    "guj",
    "hat",
    "heb",
    "hin",
    "hrv",
    "hun",
    "hye",
    "iku",
    "ind",
    "isl",
    "ita",
    "ita_old",
    "jav",
    "jpn",
    "kan",
    "kat",
    "kat_old",
    "kaz",
    "khm",
    "kir",
    "kmr",
    "kor",
    "kor_vert",
    "lao",
    "lat",
    "lav",
    "lit",
    "ltz",
    "mal",
    "mar",
    "mkd",
    "mlt",
    "mon",
    "mri",
    "msa",
    "mya",
    "nep",
    "nld",
    "nor",
    "oci",
    "ori",
    "pan",
    "pol",
    "por",
    "pus",
    "que",
    "ron",
    "rus",
    "san",
    "sin",
    "slk",
    "slv",
    "snd",
    "spa",
    "spa_old",
    "sqi",
    "srp",
    "srp_latn",
    "sun",
    "swa",
    "swe",
    "syr",
    "tam",
    "tat",
    "tel",
    "tgk",
    "tgl",
    "tha",
    "tir",
    "ton",
    "tur",
    "uig",
    "ukr",
    "urd",
    "uzb",
    "uzb_cyrl",
    "vie",
    "yid",
    "yor",
]

OCR_LANGUAGE_OPTIONS = {
    "eng",
    "afr",
    "amh",
    "ara",
    "asm",
    "aze",
    "aze_cyrl",
    "bel",
    "ben",
    "bod",
    "bos",
    "bre",
    "bul",
    "cat",
    "ceb",
    "ces",
    "chi_sim",
    "chi_tra",
    "chr",
    "cos",
    "cym",
    "dan",
    "deu",
    "deu_latf",
    "dzo",
    "ell",
    "enm",
    "epo",
    "equ",
    "est",
    "eus",
    "fao",
    "fas",
    "fil",
    "fin",
    "fra",
    "frm",
    "fry",
    "gla",
    "gle",
    "glg",
    "grc",
    "guj",
    "hat",
    "heb",
    "hin",
    "hrv",
    "hun",
    "hye",
    "iku",
    "ind",
    "isl",
    "ita",
    "ita_old",
    "jav",
    "jpn",
    "kan",
    "kat",
    "kat_old",
    "kaz",
    "khm",
    "kir",
    "kmr",
    "kor",
    "kor_vert",
    "lao",
    "lat",
    "lav",
    "lit",
    "ltz",
    "mal",
    "mar",
    "mkd",
    "mlt",
    "mon",
    "mri",
    "msa",
    "mya",
    "nep",
    "nld",
    "nor",
    "oci",
    "ori",
    "pan",
    "pol",
    "por",
    "pus",
    "que",
    "ron",
    "rus",
    "san",
    "sin",
    "slk",
    "slv",
    "snd",
    "spa",
    "spa_old",
    "sqi",
    "srp",
    "srp_latn",
    "sun",
    "swa",
    "swe",
    "syr",
    "tam",
    "tat",
    "tel",
    "tgk",
    "tgl",
    "tha",
    "tir",
    "ton",
    "tur",
    "uig",
    "ukr",
    "urd",
    "uzb",
    "uzb_cyrl",
    "vie",
    "yid",
    "yor",
}


class OcrFile(File):
    """Manages OCR-specific file options such as language configuration."""

    _DEFAULT_PAYLOAD = {
        "server_filename": None,
        "filename": None,
        "ocr_languages": "eng",
    }

    @property
    def ocr_languages(self) -> str:
        """
        Gets the OCR languages applied to the file.

        Returns:
            str: The current value. Default is "eng".
        """
        return self._get_attr("ocr_languages")

    @ocr_languages.setter
    def ocr_languages(self, value: str | list[str]):
        """
        Sets the languages to use in OCR.

        Args:
            value (str | list[str]): Comma-separated codes or list of codes. Must
                use values from OCR_LANGUAGE_OPTIONS.

        Raises:
            ValueError: If the language collection is empty.
            InvalidChoiceError: If any code is not supported.
        """
        languages = ",".join(value) if isinstance(value, list) else str(value)

        if not languages:
            raise ValueError("Languages cannot be empty")

        for code in languages.split(","):
            ChoiceValidator.validate(code, OCR_LANGUAGE_OPTIONS, "ocr_languages")
        self._set_attr("ocr_languages", languages)


class PdfOcrTask(Task[OcrFile]):
    """Handles OCR processing for PDF files using the iLovePDF API.

    The PdfOcrTask class lets you add PDF files, configure OCR languages, and
    execute recognition to extract searchable text.

    Example:
        task = PdfOcrTask(public_key, secret_key)
        task.add_file("document.pdf")
        task.execute()
        task.download("document_ocr.pdf")
    """

    _tool = "pdfocr"
    cls_file = OcrFile
