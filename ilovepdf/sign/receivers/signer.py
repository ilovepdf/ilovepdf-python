"""Module for the Signer receiver in iLovePDF signature workflows.

Defines the Signer class, which represents a signer participant in a PDF signature process.
"""

from typing import Dict, List, Optional, Union

from .receiver_abstract import ReceiverAbstract


class Signer(ReceiverAbstract):
    """Represents a signer participant in a PDF signature workflow.

    The Signer class manages the signer's information and the signature elements assigned to them.
    """

    valid_force_signature_types = ["all", "text", "sign", "image"]

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self.set_type("signer")
        self.phone: Optional[str] = None
        self.force_signature_type: Optional[str] = None
        self._elements: Dict[str, Dict[str, Union[object, list]]] = {}

    def add_elements(self, file, elements: Union[object, List[object]]):
        """
        file: an object with a get_server_filename() method
        elements: a single element or a list of elements (should have to_dict() method)
        """
        server_filename = file.get_server_filename()
        if not isinstance(elements, list):
            elements = [elements]

        if server_filename not in self._elements:
            self._elements[server_filename] = {"file": file, "elements": []}

        self._elements[server_filename]["elements"].extend(elements)
        return self

    def get_force_signature_type(self) -> Optional[str]:
        return self.force_signature_type

    def set_force_signature_type(self, force_signature_type: str):
        if force_signature_type not in self.valid_force_signature_types:
            msg = (
                f"Invalid force_signature_type: {force_signature_type}, "
                f"valid arguments are: {self.valid_force_signature_types}"
            )
            raise ValueError(msg)
        self.force_signature_type = force_signature_type
        return self

    def get_phone(self) -> Optional[str]:
        return self.phone

    def set_phone(self, phone: str):
        self.phone = phone
        return self

    def to_dict(self):
        array = super().to_dict()
        array["force_signature_type"] = self.get_force_signature_type()
        array["access_code"] = self.get_access_code()
        array["phone"] = self.get_phone()
        array["files"] = self.get_files_data()
        return array

    def get_files_data(self):
        output = []
        for server_filename, item in self._elements.items():
            elements_data = []
            for single_element in item["elements"]:
                # Assumes each element has a to_dict() method
                elements_data.append(single_element.to_dict())
            output.append(
                {"server_filename": server_filename, "elements": elements_data}
            )
        return output
