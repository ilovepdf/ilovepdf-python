"""ElementAbstract module for ilovepdf/sign/elements.

This module defines the ElementAbstract class, which serves as a base class for
elements used in the ilovepdf sign feature. It provides methods for setting and
retrieving element properties such as type, position, size, content, and page range.
"""

# pylint: disable=too-many-instance-attributes
import json


class ElementAbstract:
    """Base class for elements used in the ilovepdf sign feature.

    Provides methods for setting and retrieving element properties such as type,
    position, size, content, and page range.
    """

    VALID_X_GRAVITY_POSITIONS = ["left", "center", "right"]
    VALID_Y_GRAVITY_POSITIONS = ["top", "middle", "bottom"]

    def __init__(self):
        self.type = None
        self.position = {"x": None, "y": None}
        self.horizontal_adjustment = 0
        self.vertical_adjustment = 0
        self.pages = None
        self.size = 18
        self.content = None
        self.info = None

    def get_type(self):
        return self.type

    def set_type(self, type_):
        self.type = type_
        return self

    def get_info(self):
        if self.info:
            return json.dumps(self.info)
        return self.info

    def get_position(self):
        return self.position

    def set_gravity_position(
        self, position_x, position_y, horizontal_adjustment=0, vertical_adjustment=0
    ):
        if position_x not in self.VALID_X_GRAVITY_POSITIONS:
            raise ValueError(
                f"Invalid X value, valid positions are: {', '.join(self.VALID_X_GRAVITY_POSITIONS)}"
            )
        if position_y not in self.VALID_Y_GRAVITY_POSITIONS:
            raise ValueError(
                f"Invalid Y value, valid positions are: {', '.join(self.VALID_Y_GRAVITY_POSITIONS)}"
            )
        self.position = {"x": position_x, "y": position_y}
        self.horizontal_adjustment = horizontal_adjustment
        self.vertical_adjustment = vertical_adjustment
        return self

    def get_vertical_adjustment(self):
        return self.vertical_adjustment

    def get_horizontal_adjustment(self):
        return self.horizontal_adjustment

    def set_position(self, pos_x, pos_y):
        if pos_y > 0:
            raise ValueError("Invalid Y value: it must be a number lower or equal to 0")
        if pos_x < 0:
            raise ValueError(
                "Invalid X value: it must be a number greater or equal to 0"
            )
        self.position = {"x": pos_x, "y": pos_y}
        return self

    def get_pages(self):
        return self.pages

    def set_pages(self, pages):
        def parse_page(page):
            if "-" in page:
                firstpage, lastpage = page.split("-")
                firstpage = int(firstpage)
                lastpage = int(lastpage)
                if firstpage <= 0 or lastpage <= 0 or (lastpage < firstpage):
                    raise ValueError(f"Invalid page range '{page}'")
                return (
                    f"{firstpage}"
                    if firstpage == lastpage
                    else f"{firstpage}-{lastpage}"
                )
            if int(page) <= 0:
                raise ValueError(
                    f"Invalid page '{page}': it should be a value greater than 0"
                )
            return str(int(page))

        if isinstance(pages, str):
            pages = [p.strip() for p in pages.split(",")]
        pages = list(map(parse_page, pages))
        self.pages = ",".join(pages)
        return self

    def get_size(self):
        return self.size

    def set_size(self, size):
        if size <= 0:
            raise ValueError("Invalid size: must be a number greater than 0")
        self.size = size
        return self

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content
        return self

    def to_dict(self):
        pos = self.get_position()
        pos_str = f"{pos['x']} {pos['y']}".strip()
        return {
            "type": self.get_type(),
            "position": pos_str,
            "horizontal_position_adjustment": self.get_horizontal_adjustment(),
            "vertical_position_adjustment": self.get_vertical_adjustment(),
            "pages": self.get_pages(),
            "size": self.get_size(),
            "content": self.get_content(),
            "info": self.get_info(),
        }
