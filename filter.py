#!/usr/bin/env python
"""Schrodinger's RNG by Gaz Davidson <gaz@bitplane.net> 2013

Filters a CSV created by extract.py and outputs a stream of random numbers.
"""
import argparse
import sys

from struct import pack

def process_stream(input=sys.stdin, output=sys.stdout, format='ASCII', 
    length=0, column=0, min_samples=100):
    """todo: docstring"""

    def output(byte):
        print '0x%x' % byte,

    def get_sample(input_line):
        return int(input_line[:-1].split(',')[column])

    # each input line is one bit, output is in bytes
    max_samples = length*8 if length else sys.maxint

    # first we need to retrieve min_samples
    count   = min(max_samples, min_samples)
    backlog = [get_sample(input.readline()) for i in range(count)]
    total   = sum(backlog)
    average = total / float(count)

    # dump out the backlog
    bits  = (0 if sample < average else 1 for sample in backlog)
    for bit in bits:
       print bit,

    #
    for line in iter(input.readline, ''):
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__, 
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', default=sys.stdin,
                        help='The place to get our raw data. Defaults to stdin')
    parser.add_argument('-o', '--output', dest='output', default=sys.stdout,
                        help='A place to write (append) the output. Defaults to stdout')
    parser.add_argument('--length', dest='length', type=int, default=0,
                        help="Number of bytes to extract before we quit.")
    parser.add_argument('--column', dest='column', type=int, default=0,
                        help="The column number in the input CSV")
    parser.add_argument('--min-samples', dest='min_samples', type=int, default=100,
                        help="Number of samples to take before we know the average")

    args = parser.parse_args()

    # open any files
    open_files = []

    try:
        if type(args.input) == str:
            args.input = open(args.input, 'rt')
            open_files.append(args.input)
        if type(args.output) == str:
            args.output = open(args.output, 'wt+')
            open_files.append(args.output)

        process_stream(input=args.input, output=args.output, length=args.length,
                       column=args.column, min_samples=args.min_samples)
    finally:
        # close files 
        for f in open_files:
            if not f.closed:
                f.close()


if __name__ == '__main__':
    main()
