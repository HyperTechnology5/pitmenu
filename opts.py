#
# Options
#
CFG = {
  "width": 480,
  "height": 320,
  "mouse": True,
  "font-size": 28,
  "header": 2,
  "ext": {
    "zip": "echo zip",
    "cmd": "echo cmd",
  }
};

def _chkarg(arglst, opt, elm):
  if arglst[0][0:len(opt)] == opt:
    CFG[elm] = arglst.pop(0)[len(opt):]
    return True

  return False

def _vopts(argv):
  for k in CFG:
    if _chkarg(argv,"--" + k +"=", k):
      return True
  return False

def _chkbool(arglst,opt,elm,val):
  if arglst[0] == opt:
    CFG[elm] = val
    arglst.pop(0)
    return True
  return False

def _bopts(argv):
  for k in CFG:
    if _chkbool(argv,"--" + k , k,True):
      return True
    elif _chkbool(argv,"--no-" + k , k,False):
      return True
  return False

def _isext(argv):
  ext = "--ext."
  if not (argv[0][0:len(ext)] == ext):
    return False

  v = argv.pop(0)[len(ext):].split("=",2)
  if v == "":
    return False

  if len(v) == 1:
    if v[0] in CFG["ext"]:
      del CFG["ext"][v[0]]
  else:
    CFG["ext"][v[0]] = v[1]

  return True


def parse(argv):
  defext = CFG["ext"]
  CFG["ext"] = {}
  while len(argv) > 0:
    if not (_vopts(argv) or _isext(argv) or _bopts(argv)):
      break

  if len(CFG["ext"]) == 0:
    CFG["ext"] = defext


#def main(argv):
#  # 5. parse command line arguments
#  argv0 = argv.pop(0)
#  parse(argv)
#  for i in argv:
#    print i


#if __name__ == "__main__":
#  import sys
#  main(sys.argv)
