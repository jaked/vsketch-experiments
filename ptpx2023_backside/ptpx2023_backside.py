"""Postcard mailing helper sketch

How to use:

1) Create the following files next to the sketch script:
-`addresses.txt`: all the addresses, separated by two new lines
- `header.txt`: header text
- `message.txt`: postcard message, may contain $FirstName$, which will be replaced as you
  expect

2) Run: `vsk run postcard`
"""

from pathlib import Path
from typing import List, Tuple
import numpy as np

import vsketch

try:
    ADDRESSES = (Path(__file__).parent / "addresses.txt").read_text().split("\n\n")
except FileNotFoundError:
    ADDRESSES = ["John Doe\n123 Main St\nAnytown, USA"]

try:
    HEADER = (Path(__file__).parent / "header.txt").read_text()
except FileNotFoundError:
    HEADER = "Myself\nMy Place\nMy town, USA"


try:
    MESSAGE = (Path(__file__).parent / "message.txt").read_text()
except FileNotFoundError:
    MESSAGE = """
Jake Donham
318 Moraga St
San Francisco, CA 94122
USA








@jakedonham@sfba.social
#ptpx 2023
"""


class PostcardSketch(vsketch.SketchClass):
    addr_id = vsketch.Param(0, 0, len(ADDRESSES) - 1)
    show_lines = vsketch.Param(True)

    address_font_size = vsketch.Param(0.2, decimals=2)
    address_line_spacing = vsketch.Param(1.9, decimals=2)
    address_y_offset = vsketch.Param(1.9, decimals=2)

    message_font_size = vsketch.Param(0.2, decimals=2)
    message_line_spacing = vsketch.Param(1.2, decimals=2)
    message_y_offset = vsketch.Param(0.25, decimals=2)

    font = "futural"

    @staticmethod
    def first_name(address: str) -> str:
        lines = address.splitlines()
        name_line = lines[0].split(" ")
        # deal with abbreviated first name
        if len(name_line) > 2 and len(name_line[1]) > len(name_line[0]):
            return name_line[1]
        else:
            return name_line[0]

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("6in", "4in", landscape=False, center=False)
        vsk.scale("inch")

        address = ADDRESSES[self.addr_id]

        if self.show_lines:
            vsk.line(3, 0.5, 3, 3.75)
            vsk.rect(5.125, 0.25, 0.625, 0.625)

            for y in np.linspace(2, 3.125, 4):
                vsk.line(3.25, y + 0.0625, 5.75, y + 0.0625)

        vsk.text(
            MESSAGE,
            0.25,
            self.message_y_offset,
            width=3.0,
            size=self.message_font_size,
            line_spacing=self.message_line_spacing,
            font=self.font
        )

        vsk.text(
            address,
            3.3125,
            self.address_y_offset,
            width=3.0,
            size=self.address_font_size,
            line_spacing=self.address_line_spacing,
            font=self.font
        )

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        pass


if __name__ == "__main__":
    PostcardSketch.display()
