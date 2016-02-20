#!/bin/sh
$EMU "$@" 2>&1 | tee /tmp/emu.log 1>&2
