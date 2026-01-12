"""
Handles image to PDF conversion tasks using the iLovePDF API.

Provides the ImagePdfTask class to configure and execute image-to-PDF conversion,
allowing settings such as orientation, margin, rotation, page size, and merging
behavior.
"""

from typing import Literal

from ilovepdf.task import Task
from ilovepdf.validators import BoolValidator, ChoiceValidator, IntValidator

OrientationType = Literal["portrait", "landscape"]
ORIENTATION_OPTIONS = {"portrait", "landscape"}

PageSizeType = Literal["fit", "A4", "letter"]
PAGESIZE_OPTIONS = {"fit", "A4", "letter"}

RotateType = Literal[0, 90, 180, 270]
ROTATE_OPTIONS = {0, 90, 180, 270}


FILE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp"]


class ImagePdfTask(Task):
    """
    Handles image to PDF conversion tasks using the iLovePDF API.

    Allows configuration of orientation, margin, rotation, page size, and merging
        behavior.
    """

    _tool = "imagepdf"
    _file_extension = FILE_EXTENSIONS

    _DEFAULT_PAYLOAD = {
        "orientation": "portrait",
        "margin": 0,
        "rotate": 0,
        "pagesize": "fit",
        "merge_after": True,
    }

    @property
    def orientation(self) -> OrientationType:
        """
        Gets the current page orientation for image to PDF conversion. Default is
            'portrait'.

        Returns:
            OrientationType: The current orientation ('portrait', 'landscape').
        """
        return self._get_attr("orientation")

    @orientation.setter
    def orientation(self, value: OrientationType):
        """
        Sets the page orientation for image to PDF conversion.

        Args:
            value (OrientationType): Must be one of ORIENTATION_OPTIONS.

        Raises:
            InvalidChoiceError: If the value is not valid.
        """
        ChoiceValidator.validate(value, ORIENTATION_OPTIONS, "orientation")
        self._set_attr("orientation", value)

    @property
    def margin(self) -> int:
        """
        Gets the current page margin in points. Default is 0.

        Returns:
            int: The current page margin.
        """
        return self._get_attr("margin")

    @margin.setter
    def margin(self, value: int):
        """
        Sets the page margin in points.

        Args:
            value (int): Must be a non-negative integer.

        Raises:
            IntOutOfRangeError: If value is negative.
        """
        IntValidator.validate_non_negative(value, "margin")
        self._set_attr("margin", value)

    @property
    def rotate(self) -> RotateType:
        """
        Gets the current rotation angle for images. Default is 0.

        Returns:
            RotateType: The current rotation (0, 90, 180, or 270).
        """
        return self._get_attr("rotate")

    @rotate.setter
    def rotate(self, value: RotateType):
        """
        Sets the rotation angle for images.

        Args:
            value (RotateType): Must be one of ROTATE_OPTIONS.

        Raises:
            InvalidChoiceError: If the value is not valid.
        """
        ChoiceValidator.validate(value, ROTATE_OPTIONS, "rotate")
        self._set_attr("rotate", value)

    @property
    def pagesize(self) -> PageSizeType:
        """
        Gets the current page size for image to PDF conversion. Default is 'fit'.
        Returns:
            PageSizeType: The current page size ('fit', 'A4', 'letter').
        """
        return self._get_attr("pagesize")

    @pagesize.setter
    def pagesize(self, value: PageSizeType):
        """
        Sets the page size for image to PDF conversion.

        Args:
            value (PageSizeType): Must be one of PAGESIZE_OPTIONS.
        Raises:
            InvalidChoiceError: If the value is not valid.
        """
        ChoiceValidator.validate(value, PAGESIZE_OPTIONS, "pagesize")
        self._set_attr("pagesize", value)

    @property
    def merge_after(self) -> bool:
        """
        Gets the merge_after option. If True, merge all images into a single PDF.
            Default is True.

        Returns:
            bool: Merge mode status.
        """
        return self._get_attr("merge_after")

    @merge_after.setter
    def merge_after(self, value: bool):
        """
        Sets the merge_after option to merge all images into a single PDF if True, or
        keep separate PDFs if False.

        Args:
            value (bool): If True, merge images after conversion.
        Raises:
            InvalidChoiceError: If value is not boolean.
        """
        BoolValidator.validate(value, "merge_after")
        self._set_attr("merge_after", value)
