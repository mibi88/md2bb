"""
md2bb - A small Markdown to BBCode converter.
Target for planet-casio.com

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import convert

def planetcasio_on_end(string: str) -> str:
    return string.replace("`", "[inlinecode]`[/inlinecode]")

planetcasio = convert.Target(planetcasio_on_end)
planetcasio.code = "courier"
planetcasio.hr = "[center][color=DarkRed][b]==============[b][/color][/center]"
planetcasio.headers = [
    "[color=DarkRed][big][b][i]{0}[/i][/b][/big][/color]",
    "[color=DarkRed][b][i]- {0}[/i][/b][/color]",
    "[color=DarkRed][b]-- {0}[/b][/color]",
    "[color=DarkRed]--- {0}[/color]",
    "[color=DarkRed]---- {0}[/color]",
    "[color=DarkRed]----- {0}[/color]",
]
planetcasio.email = "{0} ({0})"