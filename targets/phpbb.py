"""
md2bb - A small Markdown to BBCode converter.
Target for phpBB forums.

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import convert

phpbb = convert.Target()

phpbb.headers = [
    "[size=200]{0}[/size]",
    "[size=190]{0}[/size]",
    "[size=180]{0}[/size]",
    "[size=170]{0}[/size]",
    "[size=160]{0}[/size]",
    "[size=150]{0}[/size]",
    "[size=140]{0}[/size]"
]
