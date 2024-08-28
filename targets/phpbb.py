"""
md2bb - A small Markdown to BBCode converter.
Target for phpBB forums.

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import convert

def phpbb_on_end(string: str) -> str:
    return string

def phpbb_list_item(string: str, diff: int, numbered: bool) -> str:
    out = ""
    if diff > 0:
        for i in range(diff):
            if numbered:
                out += "[list=ol]"
            else:
                out += "[list]"
    elif diff < 0:
        for i in range(-diff): out += "[/list]"
    if diff == 0:
        if numbered:
            out += "[/list][list=ol]"
        else:
            out += "[/list][list]"
    out += string
    return out

def phpbb_list_end(lastlevel: int) -> str:
    out = ""
    for i in range(lastlevel+1): out += "[/list]"
    return out

phpbb = convert.Target(phpbb_on_end, phpbb_list_item, phpbb_list_end)

phpbb.hr = "[center][b]==============[/b][/center]"
phpbb.code = "[tt]{0}[/tt]"
phpbb.headers = [
    "[size=200]{0}[/size]",
    "[size=190]{0}[/size]",
    "[size=180]{0}[/size]",
    "[size=170]{0}[/size]",
    "[size=160]{0}[/size]",
    "[size=150]{0}[/size]",
    "[size=140]{0}[/size]"
]
