#!/bin/sh
trap 'kill $streamPid $extractPid' EXIT
streamer -q -s 320x240 -t 126000 -c /dev/video0 -r 5 -f gray -o pipe.raw & streamPid=$!
cat pipe.raw | pypy ./extract.py --width=320 --height=240 & extractPid=$!
wait
