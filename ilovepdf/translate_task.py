"""Handles PDF translation tasks using the iLovePDF API.

Provides the TranslateTask class to configure and execute AI-powered PDF translation.
Translates PDF documents to the selected target language.
"""

from typing import Literal

from .task import Task
from .validators import ChoiceValidator

LanguageCodeType = Literal[
    "eng",
    "spa",
    "fra",
    "deu",
    "ita",
    "por",
    "rus",
    "jpn",
    "chi_sim",
    "chi_tra",
    "kor",
    "ara",
    "hin",
    "tur",
    "pol",
    "dut",
    "gre",
    "cze",
    "swe",
    "dan",
    "fin",
    "nor",
    "hun",
    "rom",
    "vie",
    "tha",
]
LANGUAGE_CODE_OPTIONS = {
    "eng",
    "spa",
    "fra",
    "deu",
    "ita",
    "por",
    "rus",
    "jpn",
    "chi_sim",
    "chi_tra",
    "kor",
    "ara",
    "hin",
    "tur",
    "pol",
    "dut",
    "gre",
    "cze",
    "swe",
    "dan",
    "fin",
    "nor",
    "hun",
    "rom",
    "vie",
    "tha",
}


class TranslateTask(Task):
    """
    Handles PDF translation tasks using the iLovePDF API.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = TranslateTask(public_key="your_public_key", secret_key="your_secret_key")
        task.add_file("document.pdf")
        task.language_input = "eng"
        task.language_output = "spa"
        task.execute()
        task.download("output_folder")
    """

    _tool = "translate"

    _DEFAULT_PAYLOAD = {
        "language_input": None,
        "language_output": None,
    }

    REQUIRED_FIELDS = ["language_input", "language_output"]

    @property
    def language_input(self) -> LanguageCodeType | None:
        """
        Gets the current source/input language.

        Returns:
            LanguageCodeType | None: The current value. Default is None.
        """
        return self._get_attr("language_input")

    @language_input.setter
    def language_input(self, value: LanguageCodeType):
        """
        Sets the source/input language for the translation.

        Args:
            value (LanguageCodeType): Must be one of the available language codes.

        Raises:
            InvalidChoiceError: If value is not one of the allowed language codes.
        """
        ChoiceValidator.validate(value, LANGUAGE_CODE_OPTIONS, "language_input")
        self._set_attr("language_input", value)

    @property
    def language_output(self) -> LanguageCodeType | None:
        """
        Gets the current target/output language.

        Returns:
            LanguageCodeType | None: The current value. Default is None.
        """
        return self._get_attr("language_output")

    @language_output.setter
    def language_output(self, value: LanguageCodeType):
        """
        Sets the target/output language for the translation.

        Args:
            value (LanguageCodeType): Must be one of the available language codes.

        Raises:
            InvalidChoiceError: If value is not one of the allowed language codes.
        """
        ChoiceValidator.validate(value, LANGUAGE_CODE_OPTIONS, "language_output")
        self._set_attr("language_output", value)
