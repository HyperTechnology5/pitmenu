#
# Simple ROM menu
#

import sys
import gui
import subprocess
import opts
import os

def add_folder(app,j,count):
  # This is a directory...
  while j[-1] == "/":
    j = j[0:-1]

  banner = j + ".png"
  if not os.path.isfile(banner):
    banner = None

  menu = app.addMenu(banner)

  roms = []
  for dirname,dirnames,filenames in os.walk(j):
    for f in filenames:
      filename = f.lower()
      for k in opts.CFG["ext"]:
        if filename[-len(k)-1:] == "."+k:
          roms.append(os.path.join(dirname,f))
          count += 1
          sys.stdout.write("\rGames found: %d" % count)
          sys.stdout.flush()
          break

  roms.sort(key=lambda s: s.lower())
  for rom in roms:
    basename = '.'.join(rom.split('.')[:-1])
    png = basename + ".png"
    if not os.path.isfile(png):
      png = None
    gamename = ''.join(basename.split('/')[-1])
    gamename.replace('_',' ')

    menu.add_element(gui.Button(gamename, png, rom))

  return count

def add_file(app,j):
  # This is a config file
  banner = j + ".png"
  if not os.path.isfile(banner):
    banner =  '.'.join(j.split('.')[:-1]) + ".png"
    if not os.path.isfile(banner):
      banner = None

  menu = app.addMenu(banner)

  fo = open(j,"r")
  for line in fo.readlines():
    v = line.strip().split("=",2)
    if (len(v) != 2):
      continue

    png = v[1] + ".png"
    if not os.path.isfile(png):
      png = '.'.join(v[1].split('.')[:-1]) + ".png"
      if not os.path.isfile(png):
        png = None

    menu.add_element(gui.Button(v[0],png, v[1]))



def buildMenu(argv, app):
  count = 0
  for j in argv:
    if os.path.isdir(j):
      count = add_folder(app,j,count)
    elif os.path.isfile(j):
      add_file(app,j)
  print "\rTotal Games Found: %d" % count

def main(argv):
  # 5. parse command line arguments
  argv0 = argv.pop(0)
  opts.parse(argv)

  # Initialize map
  # print "font-size: %d" % opts.CFG["font-size"]
  app = gui.MainWindow(int(opts.CFG["width"]), int(opts.CFG["height"]),
                       int(opts.CFG["font-size"]), not opts.CFG["mouse"],
                       int(opts.CFG["header"]))

  buildMenu(argv,app)


  # 10. scan rom dirs
  # sortid.png
  # sortid/[sortid,]something.ext
  # sortid.ini


  # sortid
  # - key | label | path

  # 20. open pygame
  # 30. prompt menu
  # 40. exit pygame
  # 50. action menu results
  # 60. goto 2.

  while True:
    r = app.run()
    print "r= %s" % r

    if (r is None) or (r == gui.R_EXIT):
      break
    if (r == ':'):
      continue
    else:
      for k in opts.CFG["ext"]:
        if r[-len(k)-1:] == "."+k:
          print "RUN %s %s %s" %  (k,opts.CFG["ext"][k], r)
          subprocess.call("%s '%s'" % (opts.CFG["ext"][k], r),shell=True)

    # subprocess.call("sh",shell=True)

  sys.exit()

if __name__ == "__main__":
  main(sys.argv)
