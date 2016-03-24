#!/bin/sh
roms=/roms/pi

log=/tmp/helper-log
######################################################################
# Configure mednafen
######################################################################
gamepad="joystick <JID>"
gp_a="00000001"
gp_b="00000000"
gp_down="00008001"
gp_left="0000c000"
gp_right="00008000"
gp_up="0000c001"
gp_start="00000009"
gp_select="00000008"
chord="/&&\\"

common_keys="
    command.exit $chord  $gamepad $gp_select~$gamepad $gp_start
    command.save_state $chord $gamepad $gp_select~$gamepad $gp_a
    command.load_state $chord $gamepad $gp_select~$gamepad $gp_b
    command.state_slot_dec $chord $gamepad $gp_select~$gamepad $gp_left
    command.state_slot_inc $chord $gamepad $gp_select~$gamepad $gp_right
    command.reset $chord $gamepad $gp_start~$gamepad $gp_a
    command.hard_reset $chord $gamepad $gp_start~$gamepad $gp_b
"
gg_keys="
    gg.input.builtin.gamepad.button1 $gamepad $gp_a
    gg.input.builtin.gamepad.button2 $gamepad $gp_b
    gg.input.builtin.gamepad.start $gamepad $gp_start
    gg.input.builtin.gamepad.down $gamepad $gp_down
    gg.input.builtin.gamepad.left $gamepad $gp_left
    gg.input.builtin.gamepad.right $gamepad $gp_right
    gg.input.builtin.gamepad.up $gamepad $gp_up
"
sms_keys="
    sms.input.port1.gamepad.fire1 $gamepad $gp_a
    sms.input.port1.gamepad.fire2 $gamepad $gp_b
    sms.input.port1.gamepad.pause $gamepad $gp_start~$gamepad $gp_select
    sms.input.port1.gamepad.down $gamepad $gp_down
    sms.input.port1.gamepad.left $gamepad $gp_left
    sms.input.port1.gamepad.right $gamepad $gp_right
    sms.input.port1.gamepad.up $gamepad $gp_up
"
nes_keys="
    nes.input.port1.gamepad.a $gamepad $gp_a
    nes.input.port1.gamepad.b $gamepad $gp_b
    nes.input.port1.gamepad.down $gamepad $gp_down
    nes.input.port1.gamepad.left $gamepad $gp_left
    nes.input.port1.gamepad.right $gamepad $gp_right
    nes.input.port1.gamepad.up $gamepad $gp_up
    nes.input.port1.gamepad.select $gamepad $gp_select
    nes.input.port1.gamepad.start $gamepad $gp_start
"
gb_keys="
    gb.input.builtin.gamepad.a $gamepad $gp_a
    gb.input.builtin.gamepad.b $gamepad $gp_b
    gb.input.builtin.gamepad.down $gamepad $gp_down
    gb.input.builtin.gamepad.left $gamepad $gp_left
    gb.input.builtin.gamepad.right $gamepad $gp_right
    gb.input.builtin.gamepad.up $gamepad $gp_up
    gb.input.builtin.gamepad.select $gamepad $gp_select
    gb.input.builtin.gamepad.start $gamepad $gp_start
"
######################################################################
gbcfg="
    -gb.xres 480 -gb.yres 320
    -gb.xscale 3.0 -gb.yscale 2.0
"
ggcfg="
    -gg.xres 480 -gg.yres 320
    -gg.xscale 3.0 -gg.yscale 2.0
"
nescfg="
    -nes.xres 480 -nes.yres 320
    -nes.xscale 1.7 -nes.yscale 1.4
    -nes.input.port1 gamepad
    -nes.input.port2 zapper
"
smscfg="
    -sms.xres 480 -sms.yres 320
    -sms.xscale 1.7 -sms.yscale 1.3
"

features="
    -gb.enable 1
    -gg.enable 1
    -nes.enable 1
    -sms.enable 1
    -gba.enable 0
    -lynx.enable 0
    -md.enable 0
    -ngp.enable 0
    -pce.enable 0
    -pcfx.enable 0
    -psx.enable 0
    -snes.enable 0
    -vb.enable 0
    -wswan.enable 0
"
common=""
#    -autosave 1
#    -input.ckdelay 0

opts="$features $common $gbcfg $ggcfg $nescfg $smscfg"


echo "######################################################################"
echo ""
echo "PitMenu ..."
echo ""
echo "######################################################################"
echo ""

echo -n "Configuring..."

mkdir /tmp/pi-mednafen /tmp/pi-config
cp -av /save/pi/* $HOME/.mednafen

# Configure audio
amixer cset numid=3 1 # 2=HDMI, 1=analogue, 0=auto
amixer sset PCM 350 # Volume 0-400?

# Check Overclocking
TURBO=OFF
if /bin/ovctl status ; then
  # OK, we are overclocked...
  TURBO=ON
  sudo mount -o remount,rw /boot
  sudo ovctl none
  sudo mount -o remount,ro /boot
fi
tools_ini=/tmp/tools.ini
cp tools.png /tmp/tools.png
sed -e "s/<ON|OFF>/$TURBO/" tools.ini > $tools_ini

mouse=--no-mouse
export EMU="/usr/games/mednafen $opts"

export \
  SDL_MOUSEDRV=TSLIB \
  SDL_MOUSEDEV=/dev/input/touchscreen \
  SDL_VIDEODRIVER=fbcon \
  SDL_FBDEV=/dev/fb1

# Figure out the joypad id
$EMU demo.zip > $log &
pid=$!
sleep 2
kill $pid
wait
pid=$(grep Joystick $log | grep 'Unique ID:' | head -1 | sed 's/^.*Unique ID: *//')
if [ -n "$pid" ] ; then
  echo "$common_keys $sms_keys $gg_keys $nes_keys $gb_keys" \
    | sed \
    -e 's/^ *//' \
    -e "s/<JID>/$pid/g" \
    > $HOME/.mednafen/mednafen-09x.cfg
fi
echo 'DONE.'

echo "Loading PITMENU..."

python pitmenu.pyc \
  --width=480 \
  --height=320 \
  --font-size=28 \
  --ext.zip=extra/runemu.sh \
  --ext.cmd=extra/runcmd.sh \
  $mouse \
  $roms/*/ \
  $tools_ini \
  about.ini
