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

    Parsed_BED = Table()
    for line in args.bed:
        parsed_line=parse_line(line)
        Parsed_BED.add_line(parse_line)

    for line in args.query:
        query=parsed_line[0]
        query_start=parsed_line[1]
        query_end=parsed_line[2]
        full_chrom=Parsed_BED.get_chrom(query)

    for line in full_chrom:
        chrom=line[0]
        start=line[1]
        end=line[2]
        if int(query_start) <= int(start) and int(query_end) >= int(end):
            print_line(line,args.outfile)

if __name__ == '__main__':
    main()
