#!/bin/sh
streamer -s 320x240 -t 126000 -c /dev/video1 -r 5 -f gray -o pipe.raw
