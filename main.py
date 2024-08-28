"""
md2bb - A small Markdown to BBCode converter.

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import convert
import argparse
import sys
from targets.planetcasio import *
from targets.phpbb import *

desc = """
Markdown to BBCode converter. If no output file is set, the BBCode will be
written to stdout.
"""

epilog = """
By Mibi88 - contact <mbcontact50@gmail.com>. Report issues at
<https://github.com/mibi88/md2bb>.
"""

targets = {
    "phpbb": phpbb,
    "planet-casio": planetcasio
}

parser = argparse.ArgumentParser(prog = "md2bb",
                                 description = desc,
                                 epilog = epilog)

parser.add_argument("file")
parser.add_argument("-o", "--output", help = "the output file")
parser.add_argument("-t", "--target", help = "the target website",
                    choices = targets, default = "phpbb")
parser.add_argument("-e", "--extra", help = "enable extra Markdown features",
                    action = "store_true")

args = parser.parse_args()

with open(args.file, "r") as file:
    converter = convert.MDConv(file.read(), targets[args.target],
                               args.extra == True)
    out = converter.parse()
    if args.output:
        with open(args.output, "w") as outfile:
            outfile.write(out)
    else:
        sys.stdout.write(out)
