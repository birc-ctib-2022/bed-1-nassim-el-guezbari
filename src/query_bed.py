"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    parse_line, print_line
)
from query import Table


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    # FIXME: put your code here

parsed_file=Table()
for line in args.bed:
    parsed_line=parse_line(line)
    parsed_file.add_line(parsed_line)

for line in args.query.redlines():
    tab_seperation = line.split("\t")
    All_lines_chrom = parsed_file.get_chrom(tab_seperation[0])
    start = int(tab_seperation[1])
    end = int(tab_seperation[2])

    for line in All_lines_chrom:
        if start <= line.chrom_start < end:
            print_line(k, args.outfile)
    

if __name__ == '__main__':
    main()
