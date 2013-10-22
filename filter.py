#!/usr/bin/env python
"""Schrodinger's RNG by Gaz Davidson <gaz@bitplane.net> 2013

Filters a CSV created by extract.py and outputs a stream of random numbers.
"""
import argparse
import itertools
import sys

from struct import pack

def process_stream(input=sys.stdin, output=sys.stdout, format='ASCII', 
    length=0, column=0, min_samples=100, delimiter=','):

    def output(byte):
        print '%02X' % byte,

    class CSVSamplerWithAverage(object):
        """A sequence generating class which takes a sequence of strings, 
        splits them by delimiter, returns the given column and keeps
        an average of the values."""
        def __init__(self, lines, column, delimiter=','):
            self.count     = 0
            self.average   = 0
            self.total     = 0
            self.lines     = lines
            self.delimiter = delimiter
            self.column    = column

        def __iter__(self):
            return self

        def next(self):
            line         = self.lines.next()
            sample       = float(line.split(self.delimiter)[self.column])
            self.total   = self.total + sample
            self.count   = self.count + 1
            self.average = self.total / self.count
            return sample

    def bits_to_bytes(bits):
        while True:
            tot = 0
            for i in range(8):
                if bits.next() == 1:
                    tot = tot + 2**i
            yield tot

    lines   = (line for line in iter(input.readline, ''))
    samples = CSVSamplerWithAverage(lines, column, delimiter)

    # length is in bytes, samples are one bit each
    max_samples = 8*length if length else sys.maxint

    # first we read until we have an average for the column we want
    # we store these samples in the backlog and process them later.
    count           = min(max_samples, min_samples)
    backlog_samples = [samples.next() for i in range(count)]

    # now we have a moving average to compare each sample against when
    # pulling bits from the source, but we don't want to throw the rest
    # away, so we join the two sources together
    all_samples = itertools.chain(backlog_samples, samples)

    # but we don't want all the samples, the user might only want to copy
    # a fixed number of bytes
    #limited_samples = (all_samples.next() for i in range(length))

    # creates a sequence of bits from a sequence of numbers.
    bits = (0 if sample < samples.average else 1 for sample in all_samples)

    for byte in bits_to_bytes(bits):
       output(byte)

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
