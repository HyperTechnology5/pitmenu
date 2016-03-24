#!/bin/sh
$EMU "$@" 2>&1 | tee /tmp/emu.log 1>&2
# Save data...
sudo mount -o remount,rw /save
cp --update -av $HOME/.mednafen/*  /save/pi
sudo mount -o remount,ro /save
