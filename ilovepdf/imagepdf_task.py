"""
Module for handling image to PDF conversion tasks for iLovePDF.
Provides the ImagePdfTask class, which allows configuration of orientation, margin,
rotation, page size, and merging behavior for image to PDF conversion.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class ImagePdfTask(ProcessTask):
    """
    Handles image to PDF conversion tasks for iLovePDF.
    Allows configuration of orientation, margin, rotation, page size, and merging behavior.
    """

    DEFAULTS = {
        "orientation": "portrait",
        "margin": 0,
        "rotate": 0,
        "pagesize": "fit",
        "merge_after": True,
    }

    VALID_ORIENTATIONS = ("portrait", "landscape")
    VALID_ROTATES = (0, 90, 180, 270)
    VALID_PAGESIZES = ("fit", "A4", "letter")

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="imagepdf")
        self._params = dict(self.DEFAULTS)

    @property
    def orientation(self):
        """Page orientation: 'portrait' or 'landscape' (default: 'portrait')."""
        return self._params["orientation"]

    @orientation.setter
    def orientation(self, value):
        if value not in self.VALID_ORIENTATIONS:
            raise ValueError("Orientation must be 'portrait' or 'landscape'")
        self._params["orientation"] = value

    @property
    def margin(self):
        """Page margin in points (default: 0)."""
        return self._params["margin"]

    @margin.setter
    def margin(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Margin must be a non-negative integer")
        self._params["margin"] = value

    @property
    def pagesize(self):
        """Page size: 'fit', 'A4', or 'letter' (default: 'fit')."""
        return self._params["pagesize"]

    @pagesize.setter
    def pagesize(self, value):
        if value not in self.VALID_PAGESIZES:
            raise ValueError("Pagesize must be 'fit', 'A4', or 'letter'")
        self._params["pagesize"] = value

    @property
    def merge_after(self):
        """
        If True, all converted images are merged into a single PDF.
        If False, each image is served as a separate PDF (default: True).
        """
        return self._params["merge_after"]

    @merge_after.setter
    def merge_after(self, value):
        self._params["merge_after"] = bool(value)

    def _to_dict(self):
        """
        Converts the task parameters to a dictionary for API submission.
        """
        data = super()._to_dict()
        data.update(self._params)
        return data
