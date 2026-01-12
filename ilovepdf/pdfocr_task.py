"""
Module for handling PDF OCR tasks using the ilovepdf API.

This module defines the PdfOcrTask class, which allows configuring and executing
Optical Character Recognition (OCR) on PDF files. Supported languages for OCR
are listed in the LANGUAGES variable.
"""

from .file import File
from .task import Task

LANGUAGES = [
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


class OcrFile(File):
    """File class for OCR tasks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ocr_languages = "eng"

    def set_languages(self, languages):
        """
        Sets the languages to use in OCR.
        :param languages: List of language codes or a comma-separated string.
        """
        if isinstance(languages, list):
            languages = ",".join(languages)
        else:
            languages = str(languages)

        if not languages:
            raise ValueError("Languages cannot be empty")

        invalid_codes = [code for code in languages.split(",") if code not in LANGUAGES]
        if invalid_codes:
            msg = (
                f"Invalid language code(s): {invalid_codes}. All values must be valid language codes. "
                f"Allowed codes are: {', '.join(LANGUAGES)}"
            )
            raise ValueError(msg)

        self.ocr_languages = languages
        return self

    def get_languages(self):
        return self.ocr_languages

    def get_file_options(self) -> dict:
        """
        Returns the file options for the current task, including OCR languages if set.
        """
        options = super().get_file_options()
        if self.ocr_languages is not None:
            options["ocr_languages"] = self.ocr_languages
        return options


class PdfOcrTask(Task[OcrFile]):
    """
    Class for the Optical Character Recognition (OCR) task on PDF files.
    Allows configuring and executing the OCR task on PDF files.
    """

    # cls_file: Type[File] = OcrFile
    # cls_file: Type[OcrFile] = OcrFile
    cls_file = OcrFile

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="pdfocr")
        self.tool = "pdfocr"
