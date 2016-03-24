
XStroke: 
Compilation dependancies:
Get build dependanceis
apt-get -y install build-essential libxft-dev libxpm-dev libxtst-dev

Compile:

cd ~
wget http://mirror.egtvedt.no/avr32linux.org/twiki/pub/Main/XStroke/xstroke-0.6.tar.gz
tar xfv xstroke-0.6.tar.gz
cd xstroke-0.6
./configure
sed -i '/^X_LIBS = / s/$/ -lXrender -lX11 -lXext -ldl/' Makefile
make
sudo make install

Add menu shortcuts:

wget https://github.com/adafruit/PiTFT_Extras/raw/master/xstroke.desktop
wget https://github.com/adafruit/PiTFT_Extras/raw/master/xstrokekill.desktop
sudo cp xstroke*.desktop /usr/share/applications/



* * *

Grab screen shots:

wget http://fbgrab.monells.se/fbgrab-1.2.tar.gz
tar -zxvf fbgrab*gz
cd fbgrab/
make
./fbgrab screenshot.png
Or press F9 from Mednafen

* * *
* * * 

Alternative Touch controls:

* Sample touch driver: https://github.com/kergoth/tslib
* xstroke code example: https://github.com/jeevesmkii/xstroke
* Algorithm: https://github.com/babraham123/gesture-demo

* * *
Listen for events, example
https://github.com/gandro/input-event-daemon
Event remaping daemon
http://users.softlab.ntua.gr/~thkala/projects/evmapd/evmapd.html

Global hot key daemon (http://manpages.ubuntu.com/manpages/utopic/man1/thd.1.html)
UBUNTU: triggerhappy
AdaFruit CupCade code
- menu and gpio driver
https://github.com/adafruit/Adafruit-Retrogame

* * *
SDL

SDL_FBACCEL
If set to 0, disable hardware acceleration in the linux fbcon driver.

SDL_AUDIODRIVER=alsa
SDL_DEBUG=1 ?
SDL_JOYSTICK_DEVICE=/dev/js*,/dev/input/event*,/dev/input/js*
SDL_LINUX_JOYSTICK="name numaxes numhats numballs"

* * * 
Mednafen

KeyBidings:
Key : action : config string
F1 : help : toggle_help
F5 : Save state : save_state
F7 : Load state : load_state
0-9 : select save slot : 0 .. 9
- : dec selected save state slot : state_slot_dec
= : inc selected save state slot : state_slot_inc
ALT+C : Cheat console : togglecheatview
ALT+T : toggle cheats : togglecheatactive
F9 : save (basic) screen snapshot : take_snapshot
Shift+F9 :  save snapshot : take_scaled_snapshot
ALT+O : Rotate screen : rotate_screen
ALT+SHIFT+[n] : Configure buttons for controller n : input_config_n
F2 : Configure command keys : input_configc
F10 : Reset : reset
F11: Hard Reset : power
Escape/F12 : Exit : exit



Other
ALT+D : debugger : toggle_debugger

## Configuration Files

Mednafen loads/saves its settings from/to a primary configuration file, named "mednafen-09x.cfg", under the Mednafen base directory. This file is created and written to when Mednafen shuts down.

Mednafen loads override settings from optional per-module override configuration files, also located directly under the Mednafen base directory. The general pattern for the naming of these user-created files is "<system>.cfg"; e.g. "nes.cfg", "pce.cfg", "gba.cfg", "psx.cfg", etc. This allows for overriding global settings on a per-module basis.

Per-game override configuration files are also supported. They should be placed in the pgconfig directory under the Mednafen base directory. Name these files like <FileBase>.<system>.cfg; e.g. "Lieutenant Spoon's Sing-a-Tune (USA).psx.cfg".

## Settings
setting : type: values : default : escr
autosave : boolean : 1|0 : 0 : auto load/save states

Special stuffs... for button overloading

F2	Activate in-game input configuration process for a command key.	input_configc

SHIFT + F2	Like F2, but after configuration completes, to activate the configured command key will require all buttons configured to it to be in a pressed state simultaneously to trigger the action. Note that keyboard modifier keys(CTRL, ALT, SHIFT) are still treated as modifiers and not discrete keys.

Especially useful in conjunction with the ckdelay setting.	

input.ckdelay	integer	0 through 99999	0	Dangerous key action delay.
The length of time, in milliseconds, that a button/key corresponding to a "dangerous" command like power, reset, exit, etc. must be pressed before the command is executed

Net play?
T : enable network play console input : togglenetview
Command line:
-connect	(n/a)	Trigger to connect to remote host after the game is loaded.
netplay.gamekey : string : security?
netplay.host : string : server host name
netplay.localplayers 
netplay.nick : string
netplay.plassword : password
netplay.port
netplay.smallfont

Try performance:
video.blit_timesync : 0|1, set to 0 to reduce latency
<system>.enable : 0 : Disable that system
<system>.forcemono : 0|1
<system>.stretch: 0  ?
<system>.xres :  0-65536 : 480
<system>.xscale : real scaling factor
<system>.yres :  0-65536 : 320
<system>.yscale : real scaling factor

**********************************************************************
MENU
<= => Switch menu
NES | UTILITIES
list [ PNG ]

- Help
- Shutdown
- Sync

HOLD:start : reset
HOLD:select : exit

A+start : save-state
A+select : state_slot_inc
B+start : load-state
B+select : state_slot_dec


SOURCE OF ROMS: http://www.freeroms.com/

* * *

Basic drawing...


nes.input.port1 gamepad
nes.input.port2 zapper

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
command.exit

SOUND:
- amixer cset numid=3 <x>
x : 2 HDMI, 1 analogue, 0 auto
- amixer sset PCM 400 <max audio>

----------------------------------------------------------------------
Add a menu to toggle turbo mode...
Digispark Pro: Pin-out diagram:
http://digispark.s3.amazonaws.com/DigisparkProDiagram2.png
18.3mm by 26.7mm

Adafruit Joystick breakout:
https://www.adafruit.com/products/512
1.5" x 1.5" x 1.25" tall

GPIO pin-outs
http://elinux.org/images/2/2a/GPIOs.png


Mausberry set-up


--- python ---
# Import the modules to send commands to the system and access GPIO pins
# http://openmicros.org/index.php/articles/94-ciseco-product-documentation/raspberry-pi/217-getting-started-with-raspberry-pi-gpio-and-python
from subprocess import call
import RPi.GPIO as gpio
 
# Define a function to keep script running
def loop():
    raw_input()
 
# Define a function to run when an interrupt is called
def shutdown(pin):
    call('halt', shell=False)
 
gpio.setmode(gpio.BOARD) # Set pin numbering to board numbering
gpio.setup(7, gpio.IN) # Set up pin 7 as an input
gpio.add_event_detect(7, gpio.RISING, callback=shutdown, bouncetime=200) # Set up an interrupt to look for button presses
 
loop() # Run the loop function to keep script running

--- bash ---
#!/bin/bash

#this is the GPIO pin connected to the lead on switch labeled OUT
GPIOpin1=23

#this is the GPIO pin connected to the lead on switch labeled IN
GPIOpin2=24

echo "$GPIOpin1" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio$GPIOpin1/direction
echo "$GPIOpin2" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio$GPIOpin2/direction
echo "1" > /sys/class/gpio/gpio$GPIOpin2/value
while [ 1 = 1 ]; do
power=$(cat /sys/class/gpio/gpio$GPIOpin1/value)
if [ $power = 0 ]; then
sleep 1
else
sudo poweroff
fi
done


## Handel virtual events
http://thiemonge.org/getting-started-with-uinput
https://github.com/Blub/netevent/wiki/Share-devices-over-the-net
Consume key events: https://github.com/wertarbyte/triggerhappy


http://superuser.com/questions/67659/linux-share-keyboard-over-network
Requires evdev kernel module:
$ cat /dev/input/by-path/*-kbd | nc <ip> 4444
On the client
$ nc -l -p 4444 > /dev/input/by-path/*-kbd


https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md


Raspberry Pi B Model
http://www.thingiverse.com/thing:725844


Simple cases:
http://www.thingiverse.com/thing:85582
http://www.thingiverse.com/thing:209100


PSP: PiStation Portable
http://www.thingiverse.com/thing:833219
- Lighted Buttons, large desing
- Model 1B
- Teensy
- Battery + Powerboost 500 + charger
- 2axis analog joystick
- 4.3" display


Game Pi
http://www.thingiverse.com/thing:871368
- Basic design
- Pi 1B
- SNES Controller
- 3.5" PiTFT
- Mausberry shutdown switch


Controller = Buttons+ Joystick
Pi
Audio
Power


# Install/Configure Wifi

apt-get install firmware-ralink  firmware-realtek wireless-tools wpasupplicant usbutils
edit /etc/network/interfaces
auto lo
iface lo inet loopback

allow-hotplug eth0
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp

edit /etc/wpa/wpa_supplicant.conf
network={
    ssid="testing"
    psk="testingPassword"
}

ifdown wlan0
ifup wlan0



Custom Kernel:
https://learn.adafruit.com/raspberry-pi-kernel-o-matic/overview
https://github.com/adafruit/Adafruit-Pi-Kernel-o-Matic

MENU Stuff
https://github.com/baochan/cupcade-launcher

AdaFruit CupCade / Retro game software
https://github.com/adafruit/Adafruit-Retrogame