import os
import pygame
from pygame.locals import *
import sys
import inputbox
import confirm

R_EXIT = "cmd.exit"

BLACK = (0, 0, 0)
WHITE = (0xFF, 0xFF, 0xFF)
GREEN = (0, 0xFF, 0)
RED  = (0xFF, 0, 0)

YELLOW = (255, 255, 153)
PALE_BLUE = (153,102,255)

BPP = 16

mX_AXIS = 0
mY_AXIS = 1
JSBTN_A = 1
JSBTN_B = 0
JSBTN_SELECT = 8
JSBTN_START = 9
THRESHOLD = 10*10+10*10

class WindowArea(object):
  def __init__(self,width,height,hide_mouse,font_size,blines):
    pygame.init()
    pygame.mouse.set_visible(not hide_mouse)

    self.width = width
    self.height = height

    self.screen = pygame.display.set_mode((width,height),0,BPP)

    pygame.display.update()

    self.font_size = font_size
    self.font = pygame.font.Font(None,font_size)

    sample_text = self.font.render('sample',True,(0,0,0))
    dims = sample_text.get_bounding_rect()
    self.block_size = dims[3] - dims[1] + font_size
    self.yoff = font_size * blines

    self.max_on_screen = (height - self.yoff)/ font_size
    self.resources = {}

  def loadimg(self,path):
    if path is None:
      return None
    if not os.path.isfile(path):
      return None

    return pygame.image.load(path)

  def getdimensions(self,element):
    label = element.label
    if label is None:
      return None

    key = "bb,%s" % label
    if key not in self.resources:
      text = self.gettext(label,YELLOW)
      padding = abs(self.font.get_descent())+3
      dims = text.get_bounding_rect()[:]
      dims[0] -= padding
      dims[1] -= padding
      dims[2] += padding*2
      dims[3] += padding*2
      self.resources[key] = dims

    return self.resources[key]

  def gettext(self,label,color):
    key = "txt,%s.(%x,%x,%x)" % (label,color[0],color[1],color[2])
    if key not in self.resources:
      text = self.font.render(label,True,color)
      self.resources[key] = text

    return self.resources[key]

  def fill(self,color):
    self.screen.fill(color)
  def blit(self,src,dst,area=None,flags=0):
    self.screen.blit(src,dst,area,flags)

class MenuElement(object):
  def __init__(self):
    """nothing"""

#class Label(MenuElement):

class Button(MenuElement):
  def __init__(self, label, imgpath, cmd):
    self.label = label
    self.imgpath = imgpath
    self.cmd = cmd
    #print "label: %s\nimgpath: %s\ncmd: %s\n" % (label,imgpath,cmd)

  def draw(self,gui,x,y):
    gui.blit(gui.gettext(self.label,BLACK),[x+2,y+2])
    gui.blit(gui.gettext(self.label,BLACK),[x+1,y+1])
    gui.blit(gui.gettext(self.label,BLACK),[x-1,y-1])
    gui.blit(gui.gettext(self.label,YELLOW), [x,y])


class Menu(MenuElement):
  def __init__(self, banner=None):
    self.banner = banner
    self.elements = []
    self.selection = 0
    self.position = 0
    self.top_showing = 0

  def add_element(self,element):
    self.elements.append(element)

  def display(self, gui):
    gui.fill(BLACK)

    img = gui.loadimg(self.elements[self.selection].imgpath)
    if img is not None:
      gui.blit(img,((gui.width-img.get_width())/2,(gui.height-img.get_height())/2))
    yoff = gui.font_size

    img = gui.loadimg(self.banner)
    if img is not None:
      gui.blit(img,((gui.width-img.get_width())/2,0))

    for index,element in enumerate(
            self.elements[self.top_showing:self.top_showing+gui.max_on_screen]):
      dims = gui.getdimensions(element)[:]
      x = dims[0]+(gui.width-dims[2])/2
      dims[0] = 0
      dims[1] += index * gui.font_size + gui.yoff
      dims[2] = gui.width

      #print "%d) dims: %d,%d,%d,%d" % (index,dims[0],dims[1],dims[2],dims[3])

      if index+self.top_showing == self.selection:
        pygame.draw.rect(gui.screen, PALE_BLUE, dims)
      element.draw(gui, x, dims[1])

    cnt = gui.font.render("%d/%d" % (self.selection+1, len(self.elements)), True, GREEN)
    gui.blit(cnt,(0,0))

    pygame.display.update()

  def click(self,gui,x,y):
    if (y < gui.yoff):
      return

    index = (y - gui.yoff)/gui.font_size + self.top_showing
    if (index < 0 or index >= len(self.elements)):
      return
    self.selection = index
    self.display(gui)

  def activate(self):
    #print "ACTIVATE %d" % self.selection
    return self.elements[self.selection].cmd

  def moveline(self,gui,sense):
    self.selection += sense
    if self.selection < 0 or self.selection >= len(self.elements):
      self.selection -= sense
      return

    if self.selection < self.top_showing or self.selection - self.top_showing  >= gui.max_on_screen:
      self.top_showing += sense

    self.display(gui)

  def movepage(self,gui,sense):
    self.top_showing += sense * gui.max_on_screen
    if self.top_showing < 0:
      self.top_showing = 0
    elif self.top_showing + gui.max_on_screen >= len(self.elements):
      self.top_showing = len(self.elements) - gui.max_on_screen
      if (self.top_showing < 0):
        self.top_showing = 0

    if self.selection < self.top_showing:
      self.selection = self.top_showing
    elif self.selection >= self.top_showing+gui.max_on_screen:
      self.selection = self.top_showing+gui.max_on_screen-1
      if self.selection >= len(self.elements):
        self.selection = len(self.elements)-1
    self.display(gui)


class MainWindow(object):
  def __init__(self, width=480, height=320, font_size = 28, hide_mouse=False,blines=2):
    self.menus = []
    self.cmenu = 0
    self.width = width
    self.height = height
    self.hide_mouse = hide_mouse
    self.font_size = font_size
    self.blines = blines

  def addMenu(self, banner):
    newMenu = Menu(banner)
    self.menus.append(newMenu)
    return newMenu

  def display(self,gui):
    self.menus[self.cmenu].display(gui)

  def horz(self,gui,sense):
    self.cmenu += sense
    if self.cmenu < 0:
      self.cmenu = len(self.menus)-1
    elif self.cmenu >= len(self.menus):
      self.cmenu = 0
    self.display(gui)

  def run(self):
    gui = WindowArea(self.width,self.height,self.hide_mouse,self.font_size,self.blines)

    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
      pygame.joystick.Joystick(i).init()

    self.display(gui)

    rcode = None
    start = None

    while rcode is None:
      for event in pygame.event.get():
        if (event.type is KEYDOWN):
          if (event.key == K_ESCAPE):
            rcode = R_EXIT
          elif event.key == K_RETURN:
            rcode = self.menus[self.cmenu].activate()
          elif event.key == K_DOWN:
            self.menus[self.cmenu].moveline(gui,1)
          elif event.key == K_UP:
            self.menus[self.cmenu].moveline(gui,-1)
          elif event.key == K_PAGEDOWN:
            self.menus[self.cmenu].movepage(gui,1)
          elif event.key == K_PAGEUP:
            self.menus[self.cmenu].movepage(gui,-1)
          elif event.key == K_LEFT:
            self.horz(gui,-1)
          elif event.key == K_RIGHT:
            self.horz(gui,1)
          # These two commands are for configuring roms and should
          # be used with a keyboard attached...
          elif event.key == K_DELETE or event.key == K_BACKSPACE:
            self._delete(gui,self.menus[self.cmenu].activate())
          elif event.key == K_r:
            self._rename(gui,self.menus[self.cmenu].activate())
        elif (event.type is JOYAXISMOTION):
          if (event.axis == mX_AXIS):
            if (event.value > 0):
              self.horz(gui,1)
            elif (event.value <0):
              self.horz(gui,-1)
          if (event.axis == mY_AXIS):
            if (event.value > 0):
              self.menus[self.cmenu].moveline(gui,1)
            elif (event.value <0):
              self.menus[self.cmenu].moveline(gui,-1)
        elif (event.type is JOYBUTTONDOWN):
          if (event.button == JSBTN_START):
            rcode = self.menus[self.cmenu].activate()
          elif (event.button == JSBTN_SELECT):
            self.menus[self.cmenu].moveline(gui,1)
          elif (event.button == JSBTN_A):
            self.menus[self.cmenu].movepage(gui,1)
          elif (event.button == JSBTN_B):
            self.menus[self.cmenu].movepage(gui,-1)

        elif (event.type is MOUSEBUTTONDOWN):
          start = event.pos
        elif (event.type is MOUSEBUTTONUP):
          end = event.pos

          startx,starty = start
          endx,endy = end
          xdif = startx - endx
          ydif = starty - endy

          if ((xdif*xdif+ydif*ydif) > THRESHOLD):
            if (xdif*xdif > ydif*ydif):
              # Horizontal swipe
              if xdif > 0:
                self.horz(gui,1)
              else:
                self.horz(gui,-1)
            else:
              # Vertical swipe
              if ydif > 0:
                #print "pgup"
                self.menus[self.cmenu].movepage(gui,1)
              else:
                #print "pgdn"
                self.menus[self.cmenu].movepage(gui,-1)
          else:
            # This is a selection
            x = (startx + endx)/2
            y = (starty + endy)/2
            self.menus[self.cmenu].click(gui,x,y)

        elif (event.type is QUIT):
          rcode = R_EXIT
      if rcode == ":":
        rcode = None

    gui = None

    pygame.quit()

    return rcode

  def _rename(self,gui,rom):
    if not os.path.isfile(rom):
      return

    dirname = os.path.dirname(rom)
    basename = os.path.basename(rom)
    ext = basename.split('.')[-1]
    basename = '.'.join(basename.split('.')[:-1])

    print "DIRNAME: " + dirname
    print "Basename: " + basename
    print "ext: " + ext

    answer = inputbox.ask(gui.screen,"ROM", basename)
    self.display(gui)

    if answer is None:
      return

    print "Rename to " + answer
    for j in [ext,"png"]:
      os.rename("%s/%s.%s" % (dirname,basename,j),"%s/%s.%s" % (dirname,answer,j))

  def _delete(self,gui,rom):
    if not os.path.isfile(rom):
      return

    dirname = os.path.dirname(rom)
    basename = os.path.basename(rom)
    ext = basename.split('.')[-1]
    basename = '.'.join(basename.split('.')[:-1])

    print "DIRNAME: " + dirname
    print "Basename: " + basename
    print "ext: " + ext

    answer = confirm.ask(gui.screen,"Delete "+basename+"?")
    if answer:
      for j in [ext,"png"]:
        os.remove("%s/%s.%s" % (dirname,basename,j))

    self.display(gui)
