#!/bin/sh
set -x
sudo mount -o remount,rw /boot
sudo ovctl turbo
sudo mount -o remount,ro /boot
sudo reboot
