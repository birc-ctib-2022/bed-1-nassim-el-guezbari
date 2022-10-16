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
    
    Parsed_bed = Table()

    for line in args.bed:
        Parsed_line= parse_line(line)
        Parsed_bed.add_line(Parsed_line)

    for line in args.query:
        query = line.split("\t")
        query_chrom = query [0]
        query_start = query [1] 
        query_end = query [2]
        full_chrom= Parsed_bed.get_chrom(query_chrom) 

        for chrom, chrom_start, chrom_end in full_chrom: 
            if int(query_start) <= int(chrom_start) and int(query_end)>= int(chrom_end):     
                print_line(line, args.outfile)

if __name__ == '__main__':
    main()