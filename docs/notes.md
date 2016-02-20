
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
