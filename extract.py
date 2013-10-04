#!/usr/bin/env python
"""Schrodinger's RNG by Gaz Davidson <gaz@bitplane.net> 2013

Extracts flashes of radiation from a camera attached to a radiation source.

Pipe raw video frame data into this script, it will output comma separated
values in the form:
    frame_number,brightness,x_position,y_position

Requires Python 2.7 or above
"""
import argparse
import sys

from struct import unpack

def process_stream(width=320, height=240, input=sys.stdin, output=sys.stdout,
                   trim_top=0, trim_bottom=0):
    """Processes a stream <todo: docstring>"""

    threshold = 50

    reader = lambda : input.read(width*height)

    frame_number = 0

    for frame_data in iter(reader, ''):
        frame_total = 0
        bright_value = 0
        bright_x, bright_y = (0, 0)

        for y in range(trim_top, height-trim_bottom):
            for x in range(width):
                pixel_value = unpack('B', frame_data[width*y + x])[0]
                frame_total = frame_total + pixel_value

                if pixel_value > bright_value:
                    # this is a new brightest pixel. Store its position
                    bright_value = pixel_value
                    bright_x, bright_y = (x, y)

        average_value = float(frame_total) / (width*height)

        if bright_value > threshold:
            print '{frame},{brightness},{x},{y}'.format(frame=frame_number,
                                                        brightness=bright_value, 
                                                        x=bright_x,
                                                        y=bright_y)

        frame_number = frame_number + 1
   

def main():
    parser = argparse.ArgumentParser(description="Observes radioactive decay in a raw video stream")
    parser.add_argument('--width', dest='width', type=int, default=320,
                        help='Width of the data stream in pixels')
    parser.add_argument('--height', dest='height', type=int, default=240,
                        help='Height of the data stream in pixels')
    parser.add_argument('-i', '--input', dest='input', default=sys.stdin,
                        help='The place to get our raw data. Defaults to stdin')
    parser.add_argument('-o', '--output', dest='output', default=sys.stdin,
                        help='A place to write the output. Defaults to stdout')
    parser.add_argument('--trim-top', dest='tt', type=int, default=0,
                        help='Ignore n rows at the top of each frame')
    parser.add_argument('--trim-bottom', dest='tb', type=int, default=0,
                        help='Ignore n rows at the bottom of each frame')

    #parser.add_argument('-f', '--format' ... ) # pixel format, selecting from list

    args = parser.parse_args()

    try:
        process_stream(width=args.width, height=args.height, input=args.input,
                       output=args.output, trim_top=args.tt, trim_bottom=args.tb)
    finally:
        pass
        # close files 
        #for f in self.openedFiles:
        #    if not f.closed:
        #        f.close()


if __name__ == '__main__':
    main()
