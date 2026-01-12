"""Module for managing files with the iLovePDF API."""

import tempfile


class File:
    """
    Represents a file uploaded to or managed by the iLovePDF API.
    """

    @staticmethod
    def get_temp_filename(extension=""):
        with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
            return temp_file.name

    def __init__(self, server_filename: str, filename: str):
        if not server_filename:
            raise ValueError("server_filename cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")
        self.server_filename = server_filename
        self.filename = filename
        self.rotate = None
        self.password = None
        self.pdf_pages = None
        self.pdf_page_number = None
        self.pdf_forms = None

    def get_file_options(self) -> dict:
        return {
            "server_filename": self.server_filename,
            "filename": self.filename,
            "rotate": self.rotate,
            "password": self.password,
            "pdf_pages": self.pdf_pages,
            "pdf_page_number": self.pdf_page_number,
            "pdf_forms": self.pdf_forms,
        }

    def set_rotation(self, degrees: int):
        if degrees not in (0, 90, 180, 270):
            raise ValueError("Rotation must be 0, 90, 180, or 270")
        self.rotate = degrees
        return self

    def set_pdf_pages(self, pdf_pages):
        self.pdf_pages = pdf_pages
        return True

    def set_pdf_page_number(self, pdf_page_number: int):
        self.pdf_page_number = pdf_page_number
        return True

    def set_password(self, password: str):
        self.password = password
        return self

    def get_server_filename(self) -> str:
        return self.server_filename

    def get_sanitized_pdf_pages(self):
        if self.pdf_pages is None:
            return None
        sanitized = []
        for pdf_page in self.pdf_pages:
            width, height = pdf_page.split("x")
            sanitized.append({"width": width, "height": height})
        return sanitized

    def get_last_page(self) -> int:
        return self.pdf_page_number

    def get_pdf_page_info(self, page_number: int):
        pdf_pages = self.get_sanitized_pdf_pages()
        if pdf_pages is None:
            return None
        return pdf_pages[page_number - 1]

    def each_pdf_form_element(self, callback):
        if not self.pdf_forms:
            return
        for pdf_form_element in self.pdf_forms:
            pdf_page_info = self.get_pdf_page_info(pdf_form_element["page"])
            callback(pdf_form_element, pdf_page_info)

    def set_server_filename(self, server_filename: str):
        if not server_filename:
            raise ValueError("server_filename cannot be empty")
        self.server_filename = server_filename
        return self

    def set_pdf_forms(self, form_params):
        if not form_params:
            raise ValueError("form_params cannot be empty")
        self.pdf_forms = form_params
        return self

    def set_filename(self, filename: str):
        if not filename:
            raise ValueError("filename cannot be empty")
        self.filename = filename
        return self
