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
    return string.replace("`", "[noeval]`[/noeval]")

def planetcasio_list_item(string: str, diff: int, numbered: bool) -> str:
    out = ""
    if diff > 0:
        for i in range(diff):
            if numbered:
                out += "[list=ol]"
            else:
                out += "[list]"
    elif diff < 0:
        for i in range(-diff): out += "[/list]"
    out += "[li]"+string+"[/li]"
    return out

def planetcasio_list_end(lastlevel: int) -> str:
    out = ""
    for i in range(lastlevel+1): out += "[/list]"
    return out

planetcasio = convert.Target(planetcasio_on_end, planetcasio_list_item,
                             planetcasio_list_end)
planetcasio.code = "[courier]{0}[/courier]"
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