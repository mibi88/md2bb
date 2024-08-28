# md2bb

A small command line markdown to BBCode converter written in python which can
target multiple websites.

It aims to be compatible with John Grubers markdown
https://daringfireball.net/projects/markdown/dingus

## Usage

Pass the filename of a markdown file to md2bb and it will convert it to BBCode.
The result will be written to stdout.

Flags:

* `-o`: Specify the output file. The BBCode will be written to it instead of
  stdout.
* `-t`: Specify the target website. md2bb is highly extendable: you can easily
  adapt it to generate BBCode for another website. Examples are in the target
  folder
* `-e`: Enable extra features. John Grubers markdown was quite limited, and
  more advanced features appeared in other parsers, such as tables. Some stuff
  also behaves differently in modern markdown parsers. This flag enables such
  features and improvements, which are not enabled by default, because as I said
  md2bb aims to be 1:1 compatible with John Grubers Markdown.

## Contributions

Contributions are welcome! Feel free to make PRs.

## Bug reports

If you encounter a bug, please provide an example (if it's about incorrect to
markdown conversion) if possible.