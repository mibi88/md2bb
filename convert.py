"""
md2bb - A small Markdown to BBCode converter.

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import re

class Target:
    def __init__(self, on_end, list_item, list_end):
        self.strong = "b"
        self.emphasis = "i"
        self.code = "[code]{0}[/code]"
        self.code_block = "[code]{0}[/code]"
        self.hr = "[hr]"
        self.headers = [
            "[h1]{0}[/h1]",
            "[h2]{0}[/h2]",
            "[h3]{0}[/h3]",
            "[h4]{0}[/h4]",
            "[h5]{0}[/h5]",
            "[h6]{0}[/h6]",
        ]
        self.url = "[url={0}]{1}[/url]"
        self.email = "[url=mailto:{0}]{1}[/url]"
        self.on_end = on_end
        self.list_item = list_item
        self.list_end = list_end
        self.quote = "quote"

class MDConv:
    def __init__(self, md: str, target: Target, extra: bool):
        self.md = md
        self.target = target
        self.extra = extra
    def parse(self) -> str:
        self.md = self.md.replace("\t", ' '*4)
        # Split the input into paragraphs
        paragraph_change = re.compile(r"(^\n)+", re.M)
        out = paragraph_change.split(self.md)
        for i in range(len(out)):
            out[i] = out[i].strip("\n")
        for i in range(len(out)):
            out[i], is_block = self.__parse_code_blocks(out[i])
            if is_block: continue
            out[i] = self.__parse_code(out[i])
        # Join the paragraphs and return the string
        return self.target.on_end("\n".join(out))
    def __parse_title(self, string: str):
        title = re.compile(r"(^.+\n(=|-)+$|#+ +.*)", re.M)
        content = re.compile(r"[^#\n]+", re.M)
        i = title.search(string)
        while i != None:
            setext = False
            type = 1
            if(i[0].endswith("=")):
                setext = True
            elif(i[0].endswith("-")):
                setext = True
                type = 2
            elif(i[0].startswith("#")):
                type = 0
                for n in i[0]:
                    if n != '#': break
                    type += 1
            if type > 0 and type <= 6:
                value = content.search(i[0])
                if value != None:
                    value = value[0].strip()
                    header = self.target.headers[type-1].format(value)
                    string = string[:i.start()] + header + string[i.end():]
                    i = title.search(string, pos = i.start()+len(header))
                else:
                    i = title.search(string, pos = i.end())
            else:
                i = title.search(string, pos = i.end())
        return string
    def __parse_tag(self, string: str, regex: re.Pattern, left: int, right: int,
                    tag_left: str, tag_right: str, starts: list) -> str:
        text = regex.split(string)
        is_tag = False
        for i in starts: is_tag |= string.startswith(i)
        if is_tag:
            string = tag_left
        else:
            string = ""
        for n in range(len(text)):
            if is_tag:
                string += text[n][left:-right]
                string += tag_right
                is_tag = not is_tag
            elif n < len(text)-1:
                string += text[n]
                string += tag_left
                is_tag = not is_tag
            else:
                string += text[n]
        return string
    def __parse_urls(self, string: str) -> str:
        # Parse URLs between angle brackets
        url = re.compile(r"<(https?|ftp):\/\/[\x20-\x7E]+>", re.M)
        email = re.compile(r"<[\x20-\x7E]+@[\x20-\x7E]+\.[\x20-\x7E]+>", re.M)
        url_long = re.compile((r"([^\\]|^)\[[\x20-\x7E]+\]" +
                               r"\((https?|ftp):\/\/[\x20-\x7E]+\ " +
                               r"?[\x20-\x7E]*\)"), re.M)
        email_long = re.compile(r"([^\\]|^)\[[\x20-\x7E]+\]\([\x20-\x7E]+" +
                                r"@[\x20-\x7E]+\ ?[\x20-\x7E]*\)", re.M)
        text = re.compile(r"\[[\x20-\x7E]+\]", re.M)
        value_long = re.compile(r"\([\x20-\x7E]+[\x20-\x7E]+[\x20-\x7E]+\ ",
                                re.M)
        value_short = re.compile(r"\([\x20-\x7E]+[\x20-\x7E]+[\x20-\x7E]+\)",
                                 re.M)
        title = re.compile(r"\ [\x20-\x7E]+\)")
        # Parse short URLs
        i = url.search(string)
        while i != None:
            string = (string[:i.start()] +
                      self.target.url.format(i[0][1:-1], i[0][1:-1]) +
                      string[i.end():])
            i = url.search(string, pos = i.end())
        # Parse short email addresses
        i = email.search(string)
        while i != None:
            string = (string[:i.start()] +
                      self.target.email.format(i[0][1:-1], i[0][1:-1]) +
                      string[i.end():])
            i = email.search(string, pos = i.end())
        # Parse long URLs
        i = url_long.search(string)
        while i != None:
            title_str = title.search(i[0])
            if title_str == None:
                title_str = ""
            else:
                title_str = title_str[0][1:-1]
            text_str = text.search(i[0])[0][1:-1]
            vsearch = value_long.search(i[0])
            if vsearch == None: vsearch = value_short.search(i[0])
            url_str = vsearch[0][1:-1]
            string = (string[:i.start()+int(i.start() != 0)] +
                      self.target.url.format(url_str, text_str, title_str) +
                      string[i.end():])
            i = url_long.search(string, pos = i.end())
        # Parse long email addresses
        i = email_long.search(string)
        while i != None:
            title_str = title.search(i[0])
            if title_str == None:
                title_str = ""
            else:
                title_str = title_str[0][1:-1]
            text_str = text.search(i[0])[0][1:-1]
            vsearch = value_long.search(i[0])
            if vsearch == None: vsearch = value_short.search(i[0])
            url_str = vsearch[0][1:-1]
            string = (string[:i.start()+int(i.start() != 0)] +
                      self.target.url.format(url_str, text_str, title_str) +
                      string[i.end():])
            i = email_long.search(string, pos = i.end())
        # TODO: labels
        return string
    def __parse(self, string: str) -> str:
        bold = re.compile(r"(\*{2}.+\*{2}|_{2}.+_{2})", re.M)
        emphasis = re.compile(r"(\*.+\*|_.+_)", re.M)
        hline = re.compile(r"( *(\*|-)){3,}", re.M)
        # Parse titles
        string = self.__parse_title(string)
        # Parse horizontal lines
        string = hline.sub(self.target.hr, string)
        # Parse lists
        string, is_list = self.__parse_lists(string)
        if not is_list:
            # Fix line jumps
            string = self.__fix_line_jumps(string)
        # Parse titles
        string = self.__parse_title(string)
        # Parse bold text
        string = self.__parse_tag(string, bold, 2, 2,
                                  f"[{self.target.strong}]",
                                  f"[/{self.target.strong}]",
                                  ["**", "__"])
        # Parse italic text
        string = self.__parse_tag(string, emphasis, 1, 1,
                                  f"[{self.target.emphasis}]",
                                  f"[/{self.target.emphasis}]",
                                  ["*", "_"])
        # Parse URLs
        string = self.__parse_urls(string)
        return string
    def __parse_code(self, string: str) -> str:
        text_list = []
        item = ""
        escaped = False
        in_code = False
        last_size = 0
        size = 0
        tag = ""
        for i in reversed(string):
            if i == '\\':
                escaped = True
            if i == '`' and not escaped:
                tag += i
                size += 1
            else:
                if not in_code:
                    if size > 0:
                        last_size = size
                        size = 0
                        text_list.append((True, item))
                        item = ""
                        in_code = not in_code
                        tag = ""
                    item = i+item
                else:
                    if size > 0:
                        if size >= last_size:
                            for n in range(size-last_size): item = "`"+item
                            size = 0
                            text_list.append((False, item))
                            item = ""
                            in_code = not in_code
                        else:
                            item = tag+item
                        tag = ""
                    item = i+item
        if item != "":
            text_list.append((not in_code, item))
        string = ""
        for i in reversed(text_list):
            if i[0]:
                string += self.__parse(i[1])
            else:
                if i[1].count("\n"):
                    string += self.target.code_block.format(i[1])
                else:
                    string += self.target.code.format(i[1])
        return string
    def __parse_code_blocks(self, string: str):
        code_indent = re.compile(r"^( {4}|\t)", re.M)

        # Parse line jumps and remove all other line jumps
        if string.startswith('\t') or string.startswith('    '):
            # It is a code block
            string = self.target.code_block.format(code_indent.sub("", string))
            return (string, True)
        return (string, False)
    def __fix_line_jumps(self, string: str):
        # Regexes
        lastquotelevel = 0
        line_jumps = re.compile(r"\ \ $", re.M)
        
        between_jumps = line_jumps.split(string)
        for n in range(len(between_jumps)):
            lines = between_jumps[n].split("\n")
            between_jumps[n] = ""
            for l in lines:
                in_quote, qlevel, l = self.__quote_stat(l)
                qdiff = qlevel-lastquotelevel
                if qdiff > 0:
                    for i in range(qdiff): l = f"[{self.target.quote}]" + l
                    lastquotelevel = qlevel
                elif qdiff < 0 and self.extra:
                    for i in range(-qdiff): l = f"[/{self.target.quote}]" + l
                    lastquotelevel = qlevel
                between_jumps[n] += l+" "
            if between_jumps[n] != "":
                between_jumps[n] = between_jumps[n][:-1]
        string = "\n".join(between_jumps).strip("\n")
        for l in range(lastquotelevel): string += f"[/{self.target.quote}]"
        return string
    def __parse_lists(self, string: str) -> str:
        # Handle lists
        is_list_start = re.compile(r"( |\t)*(\*|-|\+|[0-9]+\.)( |\t)+", re.M)
        in_list = is_list_start.match(string)
        if in_list: in_list = in_list.start() == 0
        else: in_list = False
        if not in_list:
            return (string, False)
        lines = string.split("\n")
        string = ""
        lastlevel = -1
        lastqlevel = 0
        diff = 0
        item = ""
        numbered = False
        items = 0
        for i in lines:
            itemstart = is_list_start.match(i)
            if itemstart: itemstart = itemstart.start() == 0
            else: itemstart = False
            if string == "" and item == "":
                # It is the beginning of an item.
                indent = len(i)-len(i.lstrip())
                level = indent//4+int(indent%4 > 0)
                diff = level-lastlevel
                numbered = i.lstrip(" \t")
                if len(numbered) > 0:
                    numbered = numbered[0] in "0123456789"
                else:
                    numbered = False
                item += i.lstrip(" \t*+-0123456789.")
            elif itemstart:
                for l in range(lastqlevel): item += f"[/{self.target.quote}]"
                string += self.target.list_item(item, diff, numbered)
                items += 1
                lastqlevel = 0
                lastlevel = level
                indent = len(i)-len(i.lstrip())
                level = indent//4+int(indent%4 > 0)
                diff = level-lastlevel
                if diff:
                    numbered = i.lstrip(" \t")
                    if len(numbered) > 0:
                        numbered = numbered[0] in "0123456789"
                    else:
                        numbered = False
                item = i.lstrip(" \t*+-0123456789.")
            else:
                if items == 0 or self.extra:
                    in_quote, qlevel, i = self.__quote_stat(i)
                    qdiff = qlevel-lastqlevel
                    if qdiff > 0:
                        for l in range(qdiff): i = f"[{self.target.quote}]" + i
                        lastqlevel = qlevel
                    elif qdiff < 0 and self.extra:
                        for l in range(-qdiff):
                            i = f"[/{self.target.quote}]" + i
                        lastqlevel = qlevel
                if item.endswith("  "):
                    item = item.rstrip(" ")
                    item += "\n"+i.lstrip(" >")
                else:
                    item = item.rstrip(" ")
                    item += " "+i.lstrip(" >")
        for l in range(lastqlevel): item += f"[/{self.target.quote}]"
        string += self.target.list_item(item, diff, numbered)
        string += self.target.list_end(level)
        return (string, True)
    def __quote_stat(self, string: str) -> tuple:
        quoteinfo = re.compile(r"^[ >]+", re.M)
        if string.strip().startswith(">"):
            levels = quoteinfo.search(string)[0].count(">")
            return (True, levels, string.lstrip(" >"))
        return (False, 0, string)
