# md2bb

A small command line markdown to BBCode converter written in python which can
target multiple websites.

## Usage

Pass the filename of a markdown file to md2bb and it will convert it to BBCode.
The result will be written to stdout.

Flags:

* `-o`: Specify the output file. The BBCode will be written to it instead of
  stdout.
* `-t`: Specify the target website. md2bb is highly extendable: you can easily
  adapt it to generate BBCode for another website. Examples are in the target
  folder

## Contributions

Contributions are welcome! Feel free to make PRs.

## Bug reports

If you encounter a bug, please provide an example (if it's about incorrect to
markdown conversion) if possible.