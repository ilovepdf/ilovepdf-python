"""ilovepdf package initialization."""

from . import exceptions
from .compress_task import CompressTask
from .extract_task import ExtractTask
from .file import File
from .htmltopdf_task import HtmlToPdfTask
from .ilovepdf_api import Ilovepdf
from .imagepdf_task import ImagePdfTask
from .merge_task import MergeTask
from .office_pdf_task import OfficePdfTask
from .pdfocr_task import PdfOcrTask
from .pdftopdfa_task import PdfToPdfATask
from .protect_task import ProtectTask
from .repair_task import RepairTask
from .rotate_task import RotateTask
from .sign_task import SignTask
from .split_task import SplitTask
from .task import Task
from .unlock_task import UnlockTask
from .watermark_task import WatermarkTask

__all__ = [
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
    "PdfOcrTask",
    "ProtectTask",
    "RepairTask",
    "RotateTask",
    "SignTask",
    "SplitTask",
    "UnlockTask",
    "WatermarkTask",
]
