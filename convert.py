"""
md2bb - A small Markdown to BBCode converter.

by Mibi88

This software is licensed under the Unlicense.

It aims to be compatible with Markdown 1.0.1:
https://daringfireball.net/projects/markdown/dingus
"""

import re

class Target:
    def __init__(self):
        self.strong = "b"
        self.emphasis = "i"
        self.code = "code"
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

class MDConv:
    def __init__(self, md: str, target: Target):
        self.md = md
        self.target = target
    def parse(self) -> str:
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
        return "\n".join(out)
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
                content = content.search(i[0])
                if content != None:
                    content = content[0].strip()
                    header = self.target.headers[type-1].format(content)
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
        if is_tag:
            string += tag_right
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
            text_str = text.search(i[0])[0][1:-1]
            vsearch = value_long.search(i[0])
            if vsearch == None: vsearch = value_short.search(i[0])
            url_str = vsearch[0][1:-1]
            string = (string[:i.start()+int(i.start() != 0)] +
                      self.target.url.format(url_str, text_str) +
                      string[i.end():])
            i = url_long.search(string, pos = i.end())
        # Parse long email addresses
        i = email_long.search(string)
        while i != None:
            text_str = text.search(i[0])[0][1:-1]
            vsearch = value_long.search(i[0])
            if vsearch == None: vsearch = value_short.search(i[0])
            url_str = vsearch[0][1:-1]
            string = (string[:i.start()+int(i.start() != 0)] +
                      self.target.url.format(url_str, text_str) +
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
        # Fix line jumps
        string = self.__fix_line_jumps(string)
        # Parse titles
        string = self.__parse_title(string)
        # Parse horizontal lines
        string = hline.sub(self.target.hr, string)
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
        code_start = re.compile(r"[^\\]?`+", re.M)
        i = code_start.search(string)
        tag_list = []
        while i != None:
            start = i.start()
            item = i[0]
            if item[0] != '`':
                item = item[1:]
                start += 1
            tag_list.append((start, i.end(), item))
            i = code_start.search(string, pos = i.end())
        
        in_code = False
        tag_len = 0
        last_code = 0
        code_start = f"[{self.target.code}]"
        code_end = f"[/{self.target.code}]"
        for i in reversed(tag_list):
            if in_code:
                if len(i[2]) >= tag_len:
                    string = (self.__parse(string[:i[0]]) +
                              string[i[0]:last_code] +
                              self.__parse(string[last_code:]))
                    string = string[:i[0]] + code_start + string[i[0]+tag_len:]
                    in_code = not in_code
            else:
                tag_len = len(i[2])
                string = string[:i[0]] + code_end + string[i[1]:]
                in_code = not in_code
                last_code = i[0] + len(code_end)
        if not in_code:
            string = string[:last_code] + self.__parse(string[last_code:])
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
        line_jumps = re.compile(r"\ \ $", re.M)
        
        between_jumps = line_jumps.split(string)
        for n in range(len(between_jumps)):
            between_jumps[n] = between_jumps[n].strip("\n")
            between_jumps[n] = between_jumps[n].replace("\n", " ")
        string = "\n".join(between_jumps).strip("\n")
        return string
            
