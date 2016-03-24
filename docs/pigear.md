# Creating a Portable Gaming Station

Parts:

- [Raspberry Pi B](https://www.raspberrypi.org/)
- [PiTFT](https://www.adafruit.com/products/2097), allthough other
  options are possible.
- [PiFace Shim RTC](http://www.modmypi.com/raspberry-pi/breakout-boards/raspberry-pi-(official)/piface-shim-rtc-real-time-clock),
  This is optional, but I like it.

It uses [Mednafen](http://mednafen.fobby.net/) for emulation.
Mednafen supports a number of systems, but because of the hardware
selection, this build only targets the following systems:

- nes : Nintendo Entertaiment System (Only with Turbo/Overclocking)
- gb/gbc : Gameboy / Gameboy Color
- sms : SEGA Master System
- gg : Game Gear

The software supports also the following systems, but with the
Raspberry Pi B, performance is quite poor:

- snes : Super Nintendo Entertaiment Systems
- pce : TurboGfx 16
- pce_fast : SuperGrafx
- ngp : NeoGeo Pocket
- wswan : WonderSwan
- psx : PlayStation 1
- vb : Virtual Boy
- pcfx : PC_FX
- md : Sega Genesis / Mega Drive
- lynx : Atari Lynx
- gba : Gameboy Advance


# Base Image

We use [minbian](https://minibianpi.wordpress.com/) as a starting
point as it is a very lean Raspbian image.

Get image from the [Download Page](https://minibianpi.wordpress.com/download/)

1. write to SD card
2. resize partition
  - set root to 2GB
  - e2fsck -f dev ; resize2fs dev
3. add swap 512MB : mkswap (OPTIONAL)
4. add save partition: 256MB (Preferred)
5. add data partition (rest of the SD card)
  - `mke2fs -L data`

Mount and tweak config.txt

# Tweak config.txt

Refer to [config.txt reference](https://www.raspberrypi.org/documentation/configuration/config-txt.md)

Useful settings:

    # We are using the PiTFT Framebuffer, so GPU memory is hardly used
    gpu_mem=16
    # Assume HDMI is plugged in
    hdmi_force_hotplug=1
    # 1= nosound, 2=with sound
    hdmi_drive=1
    # These provide monitor resolutions DMT: 1360x768 (V7 monitor)
    hdmi_group=2
    hdmi_mode=39

Now we are ready to boot the SD card.

Boot the SD card, the default login is:

    root:raspberry

# Basic Configuration

Change pasword...

    passwd
    apt-get update
    apt-get install raspi-config

## Update software/firmware

This step while desirable, is currently (as of 01/03/2016) not
working.  The right kernel modules fail to load.

    apt-get install rpi-update
    rpi-update # to update firmware to latest

## Network Configuration

Configure network, modify `/etc/network/interfaces`, change:

    auto eth0

to

    allow-hotplug eth0

This is because the network cable is not always connected.

Change hostname:

    /etc/hosts
    /etc/hostname

# Configure PiTFT

Adding adafruit repositories:

    wget -O- http://apt.adafruit.com/add-pin | bash

Install the kernel:

    apt-get install raspberrypi-bootloader

Append to `/boot/config.txt`

    [pi1]
    device_tree=bcm2708-rpi-b-plus.dtb
    [pi2]
    device_tree=bcm2709-rpi-2-b.dtb
    [all]
    dtparam=spi=on
    dtparam=i2c1=on
    dtparam=i2c_arm=on
    dtoverlay=pitft35r,rotate=90,speed=42000000,fps=20

Reboot... When the Pi restarts, the attached PiTFT should start out
all white and then turn black. That means the kernel found the display
and cleared the screen. If the screen did not turn black, that means
that likely there's something up with your connection or kernel
install. Solder anything that needs resoldering!

Add to `/etc/modules`

    stmpe-ts

Add to `/etc/udev/rules.d/95-stmpe.rules`

    SUBSYSTEM=="input", ATTRS{name}=="stmpe-ts", ENV{DEVNAME}=="*event*", SYMLINK+="input/touchscreen"

REBOOT and check dmesg

    apt-get install evtest tslib libts-bin

Manual Touch Screen calibration

    TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate

Display testing

    TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_test

Switch to console:

Add to `/boot/cmdline.txt`  (after rootwait)

    fbcon=map:10 fbcon=font:VGA8x8

Configure console:

    apt-get install kbd
    dpkg-reconfigure console-setup

- Encoding to use: UTF-8
- Character set to support: Guess
- Font for the console: Terminus
- Font size: 6x16

Disable Console blanking, editing  `/etc/kbd/config`:

    BLANK_TIME=0

Control Back-lit

    apt-get install wiringpi

    gpio -g mode 18 pwm
    gpio -g pwm 18 100 # dim...
    gpio -g pwm 18 1023 # max brightness
    gpio -g pwm 18 850 # min usable brightness
    gpio -g pwm 18 0 # backlight off


## HW Clock

Install HW Clock
([PiFace Shim RTC](https://github.com/piface/PiFace-Real-Time-Clock)).
Full instructions are here:
[PiFaceClockGuide](http://www.piface.org.uk/assets/piface_clock/PiFaceClockguide.pdf)

    apt-get install i2c-tools ntpdate
    raspi-config

Goto Advanced Options and enable I2C.

Check if the RTC can be found:

    i2cdetect 1

RTC should be detected at `6f`.

Add to `/etc/rc.local`

    modprobe i2c-dev
    # Calibrate the clock (default: 0x47). See datasheet for MCP7940N
    i2cset -y 1 0x6f 0x08 0x47
    modprobe i2c:mcp7941x
    echo mcp7941x 0x6f > /sys/class/i2c-dev/i2c-1/device/new_device
    hwclock -s

Setup Timezone

    dpkg-reconfigure tzdata

This is no longer needed:

    insserv -r fake-hwclock

Make sure time is right:

    ntpdate <ntp-server>
    hwclock -w

## Watchdog Service

Watchdog, should make it reboot if it hangs (do this before overclocking!)

    apt-get install watchdog
    add bcm2708_wdog to /etc/modules
    update-rc.d watchdog defaults

Edit `/etc/watchdog.conf` and uncomment

    max-load-1
    watchdog-device

Activate:

    service watchdog start

## Run as non-root (normal user)

Install sudo:

    apt-get install sudo

ADD TO SUDOERS:

    %sudo   ALL=(ALL:ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /bin/mount

Create user:

    useradd -m pi
    passwd pi
    usermod -a -G video,input,audio,sudo,tty pi

Configure autologin:

Use `raspi-config` boot options

From your Desktop system:

    ssh-copy-id pi@minibian1
    # The next one is optional
    ssh-copy-id root@minibian1

To deploy SSH public keys.  This is needed by the deployment
scripts...


# Configure Additional Software

## Install PYGAME

Downgrade sdl to the wheezy version.  The current SDL version does not
work with pygame in combination with touchscreen.

    #enable wheezy package sources
    echo "deb http://archive.raspbian.org/raspbian wheezy main
    " > /etc/apt/sources.list.d/wheezy.list
    #set stable as default package source (currently jessie)
    echo "APT::Default-release \"stable\";
    " > /etc/apt/apt.conf.d/10defaultRelease
    #set the priority for libsdl from wheezy higher then the jessie package
    echo "Package: libsdl1.2debian
    Pin: release n=jessie
    Pin-Priority: -10
    Package: libsdl1.2debian
    Pin: release n=wheezy
    Pin-Priority: 900
    " > /etc/apt/preferences.d/libsdl
    #install
    apt-get update
    apt-get -y --force-yes install libsdl1.2debian/wheezy

    aptget install python-pygame

## MEDNAFEN

    apt-get install mednafen

# Set-up Read-Only root

Switch to busybox syslog (for use of memory buffered logs)

    apt-get install busybox-syslogd
    dpkg --purge rsyslog

Remove some startup scripts:

    insserv -r bootlogs

Modify `/etc/fstab` and add `ro` to mount points and also mount `/tmp`

    tmpfs             /tmp            tmpfs   defaults     0       0

Make sure that `/tmp` is empty before rebooting

Make dhclient write its leases file to `/tmp` instead of `/var/lib/dhcp/`:

    rm -rf /var/lib/dhcp/
    ln -s /tmp /var/lib/dhcp

Also, make sure SUDO works properly (we need it).
Prep: pi user should use "sudo" at least once...

    rm -rf /var/lib/sudo/ts
    ln -s /tmp /var/lib/sudo/ts

Add to /etc/rc.local

    mkdir /tmp/sudo-ts
    chmod 700 /tmp/sudo-ts

Reboot!

# Configure Software

Make sure the menu autostarts automatically, add to `$HOME/.profile`:

    if [ $(tty) = /dev/tty1 ] ; then
      ( cd pitmenu && ./helper.sh )
    fi

Modify `/etc/fstab` and confirm that `/data` and `/save` partitions
are mounted properly (`ro`).




- copy `ovctl.sh` to `/bin` and add to `sudoers`
