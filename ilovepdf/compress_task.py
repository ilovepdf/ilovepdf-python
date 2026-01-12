"""
CompressTask module for iLovePDF Python API.
Provides functionality to compress PDF files with selectable compression levels.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class CompressTask(ProcessTask):
    """
    CompressTask for iLovePDF Python API.
    Handles PDF compression tasks with different compression levels.
    """

    COMPRESSION_LEVEL_VALUES = ("extreme", "recommended", "low")

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="compress")
        self.compression_level = "recommended"
        self.files = []
        self.task_id = None
        self.status = None
        self.status_message = None

    def set_compression_level(self, level: str):
        if level not in self.COMPRESSION_LEVEL_VALUES:
            mesg = f'Invalid compression level "{level}". Must be one of: {", ".join(self.COMPRESSION_LEVEL_VALUES)}'
            raise ValueError(mesg)
        self.compression_level = level
        return self

    def _to_dict(self):
        # Merge CompressTask-specific options with Task options
        base = super()._to_dict()
        base["compression_level"] = self.compression_level
        return base
