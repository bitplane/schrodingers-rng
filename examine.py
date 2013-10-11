#!/usr/bin/env python

import sys

from matplotlib import pyplot as plt

filename = './testdata.csv'

def main():
    # sometimes we've stopped and started the random number generator
    # so the last frame number is after the next one, we skip these frames
    lastframe    = sys.maxint
    frame_diffs  = []
    x_positions  = []
    y_positions  = []
    brightnesses = []

    with open(filename) as fin:
        for line in fin:
            (frame, brightness, x, y) = [int(s) for s in line[:-1].split(',')]
            if lastframe < frame:
                frame_diffs.append(frame - lastframe)
                x_positions.append(x)
                y_positions.append(y)
                brightnesses.append(brightness)

            lastframe = frame

    # plot some stuff...
    plt.figure(figsize=(10,7), dpi=100)
    plt.scatter(x_positions, y_positions, brightnesses)
    plt.savefig('out.png')
    

if __name__=='__main__':
    main()
