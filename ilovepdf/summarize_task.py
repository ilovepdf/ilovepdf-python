"""Handles PDF summarization tasks using the iLovePDF API.

Provides the SummarizeTask class to configure and execute AI-powered PDF summarization.
Generates concise summaries of PDF documents in the selected language and format.
"""

from typing import Literal

from .task import Task
from .validators import ChoiceValidator

LanguageType = Literal[
    "en",
    "es",
    "fr",
    "de",
    "it",
    "pt",
    "ja",
    "ru",
    "ko",
    "zh-cn",
    "zh-tw",
    "ar",
    "bg",
    "ca",
    "nl",
    "el",
    "hi",
    "id",
    "ms",
    "pl",
    "sv",
    "th",
    "tr",
    "uk",
    "vi",
]
LANGUAGE_OPTIONS = {
    "en",
    "es",
    "fr",
    "de",
    "it",
    "pt",
    "ja",
    "ru",
    "ko",
    "zh-cn",
    "zh-tw",
    "ar",
    "bg",
    "ca",
    "nl",
    "el",
    "hi",
    "id",
    "ms",
    "pl",
    "sv",
    "th",
    "tr",
    "uk",
    "vi",
}

OutputFormatType = Literal["pdf", "md"]
OUTPUT_FORMAT_OPTIONS = {"pdf", "md"}


class SummarizeTask(Task):
    """
    Handles PDF summarization tasks using the iLovePDF API.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = SummarizeTask(public_key="your_public_key", secret_key="your_secret_key")
        task.add_file("document.pdf")
        task.execute()
        task.download("output_folder")
    """

    _tool = "summarize"

    _DEFAULT_PAYLOAD = {
        "language": "en",
        "output_format": "pdf",
    }

    @property
    def language(self) -> LanguageType:
        """
        Gets the current language.

        Returns:
            LanguageType: The current value. Default is "en".
        """
        return self._get_attr("language")

    @language.setter
    def language(self, value: LanguageType):
        """
        Sets the language for the summary.

        Args:
            value (LanguageType): Must be one of the available language codes.

        Raises:
            InvalidChoiceError: If value is not one of the allowed languages.
        """
        ChoiceValidator.validate(value, LANGUAGE_OPTIONS, "language")
        self._set_attr("language", value)

    @property
    def output_format(self) -> OutputFormatType:
        """
        Gets the current output format.

        Returns:
            OutputFormatType: The current value. Default is "pdf".
        """
        return self._get_attr("output_format")

    @output_format.setter
    def output_format(self, value: OutputFormatType):
        """
        Sets the output format for the summary.

        Args:
            value (OutputFormatType): Must be one of "pdf" or "md".

        Raises:
            InvalidChoiceError: If value is not one of the allowed formats.
        """
        ChoiceValidator.validate(value, OUTPUT_FORMAT_OPTIONS, "output_format")
        self._set_attr("output_format", value)
