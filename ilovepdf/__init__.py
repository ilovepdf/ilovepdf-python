"""ilovepdf package initialization."""

__version__ = "1.0.0"

from . import exceptions
from .compress_task import CompressTask
from .editpdf_task import EditPdfTask
from .extract_task import ExtractTask
from .file import File
from .htmltopdf_task import HtmlToPdfTask
from .ilovepdf_api import Ilovepdf
from .imagepdf_task import ImagePdfTask
from .merge_task import MergeTask
from .office_pdf_task import OfficePdfTask
from .pagenumbers_task import PageNumbersTask
from .pdfmarkdown_task import PdfMarkdownTask
from .pdfocr_task import PdfOcrTask
from .pdftojpg_task import PdfToJpgTask
from .pdftopdfa_task import PdfToPdfATask
from .protect_task import ProtectTask
from .repair_task import RepairTask
from .rotate_task import RotateTask
from .sign_task import SignTask
from .smart_split_task import SmartSplitTask
from .split_task import SplitTask
from .summarize_task import SummarizeTask
from .task import Task
from .translate_task import TranslateTask
from .unlock_task import UnlockTask
from .validate_pdfa_task import ValidatePdfATask
from .watermark_task import WatermarkTask

__all__ = [
    "__version__",
    "exceptions",
    "CompressTask",
    "ExtractTask",
    "File",
    "Task",
    "Ilovepdf",
    "ImagePdfTask",
    "HtmlToPdfTask",
    "MergeTask",
    "OfficePdfTask",
    "PdfToPdfATask",
    "PdfMarkdownTask",
    "PdfOcrTask",
    "ProtectTask",
    "RepairTask",
    "RotateTask",
    "SignTask",
    "SmartSplitTask",
    "SplitTask",
    "SummarizeTask",
    "TranslateTask",
    "UnlockTask",
    "WatermarkTask",
    "PdfToJpgTask",
    "PageNumbersTask",
    "ValidatePdfATask",
    "EditPdfTask",
]
