#!/bin/sh
#
# Over-clocking control
# Should go to /bin/ovctl, and added to sudoers
#
CONFIG=/boot/config.txt

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end
if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

clear_config_var() {
  lua - "$1" "$2" <<EOF > "$2.bak"
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
for line in file:lines() do
  if line:match("^%s*"..key.."=.*$") then
    line="#"..line
  end
  print(line)
end
EOF
mv "$2.bak" "$2"
}

get_config_var() {
  lua - "$1" "$2" <<EOF
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
local found=false
for line in file:lines() do
  local val = line:match("^%s*"..key.."=(.*)$")
  if (val ~= nil) then
    print(val)
    found=true
    break
  end
end
if not found then
   print(0)
end
EOF
}

set_turbo() {
  set_overclock Turbo 1000 500 600 6
  return $?
}

set_overclock() {
  [ -e $CONFIG ] &&
  set_config_var arm_freq $2 $CONFIG &&
  set_config_var core_freq $3 $CONFIG &&
  set_config_var sdram_freq $4 $CONFIG &&
  set_config_var over_voltage $5 $CONFIG &&
  return 0
  return 1
}

clear_overclock () {
  [ -e $CONFIG ] &&
  clear_config_var arm_freq $CONFIG &&
  clear_config_var core_freq $CONFIG &&
  clear_config_var sdram_freq $CONFIG &&
  clear_config_var over_voltage $CONFIG &&
  return 0
  return 1
}

is_overclock() {
  [ ! -e $CONFIG ] && return 1
  grep -q ^over_voltage $CONFIG && grep -q ^arm_freq $CONFIG && return 0
}

case "$1" in
  status)
    if is_overclock ; then
      echo "OVERCLOCKED!"
      exit 0
    fi
    exit 1
    ;;
  turbo)
    if set_turbo ; then
      echo "Switched to TURBO mode"
      exit 0
    else
      echo "Error switching TURBO"
      exit 1
    fi
    ;;
  none)
    if clear_overclock ; then
      echo "Cleared overclocking"
      exit 0
    else
      echo "Error swithcing TURBO off"
      exit 1
    fi
    ;;
  *)
    echo "Usage: $0 status|turbo|none"
    exit 1
    ;;
esac
