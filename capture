#!/bin/sh

# load settings from configuration file
MY_DIR=$(dirname $(readlink -f $0))

if [ ! -e "$MY_DIR/config.conf" ]; then
  echo "Please run ./configure.sh to create config.conf"
  exit
fi

. $MY_DIR/config.conf


# Create a pipe because streamer doesn't support streaming to stdout
if [ ! -p "$MY_DIR/pipe.raw" ]; then
  mkfifo "$MY_DIR/pipe.raw"
fi

# kill both commands if one of them exits
trap 'kill $streamPid $extractPid' EXIT

# stream the data to disk
streamer -q -s 320x240 -t 126000 -c $DEVICE -r 5 -f gray -o $MY_DIR/pipe.raw & streamPid=$!
cat pipe.raw | $PYTHON ./extract.py --width=320 --height=240 --trim-top=1 & extractPid=$!
wait
