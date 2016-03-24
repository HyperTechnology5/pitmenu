#!/bin/sh
#
# Simple deployment script
#
system=minibian2
ruser=pi

exec 3>&1
srcdir=$(dirname $(readlink -f $0))
pitmenu=$(dirname $srcdir)
workdir=$(mktemp -d)
trap "rm -rf $workdir" EXIT

(
  rpc() {
    echo "$@" 1>&4
  }
  exec 4>&1 1>&3

  rpc sudo mount -o remount,rw /
  ovctl=$srcdir/scripts/ovctl.sh
  if [ -f $ovctl ] ; then
    scp $ovctl $ruser@$system:/tmp/ovctl
    rpc sudo install -m 755 -g 0 -u 0 /tmp/ovctl /bin/ovctl
  fi


  cp $pitmenu/*.py $workdir
  python -m compileall $workdir/*.py

  rpc mkdir -p pitmenu
  scp -r \
    $workdir/*.pyc $pitmenu/about.* $pitmenu/LICENSE $pitmenu/cmd.exit.png \
    $srcdir/demo.zip \
    $srcdir/helper.sh $srcdir/tools.* $srcdir/extra \
    $ruser@$system:pitmenu

  rpc chmod 755 pitmenu/helper.sh

  rpc sudo mount -o remount,ro /
) | ssh -T -o 'BatchMode yes' $ruser@$system
