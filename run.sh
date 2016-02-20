#!/bin/sh
roms=$HOME/Downloads/pi/roms
emu="$HOME/Downloads/m/mednafen/src/mednafen"

python pitmenu.py \
  --width=480 \
  --height=320 \
  --font-size=28 \
  --ext.zip=$emu \
  $roms/*/ \
  about.ini
rm -f *.pyc
