"""Handles PDF smart split tasks using the iLovePDF API.

Provides the SmartSplitTask class to intelligently split PDF files based on
content analysis using AI. The task identifies natural document sections
and splits accordingly.
"""

from ilovepdf.validators import StringValidator

from .task import Task


class SmartSplitTask(Task):
    """
    Handles PDF smart split tasks using the iLovePDF API.

    Smart Split uses AI to analyze PDF content and identify natural sections
    for splitting, making it easier to separate chapters, sections, or other
    logical divisions in documents.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = SmartSplitTask(
            public_key="your_public_key", secret_key="your_secret_key"
        )
        task.add_file("/path/to/document.pdf")
        task.prompt = "Split at chapter boundaries"
        task.execute()
        task.download("/path/to/output_folder")
    """

    _tool = "splitsmart"

    _DEFAULT_PAYLOAD = {
        "prompt": None,
    }

    REQUIRED_FIELDS = ["prompt"]

    @property
    def prompt(self) -> str | None:
        """
        Gets the current prompt for the smart split task.

        Returns:
            str | None: The current value. Default is None.
        """
        return self._get_attr("prompt")

    @prompt.setter
    def prompt(self, value: str):
        """
        Sets the prompt for the smart split task.

        Args:
            value (str): The prompt that guides the AI to identify natural
                document sections for splitting.

        Raises:
            TypeError: If the provided value is not a string.
            ValueError: If the provided value is empty.
        """
        StringValidator.validate(value, "prompt")
        self._set_attr("prompt", value)
