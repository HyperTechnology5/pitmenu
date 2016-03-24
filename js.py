import pygame
from pygame.locals import *

WIDTH = 480
HEIGHT = 320
BPP = 32
FONT_SIZE = 32
BGCOLOR = (0,129,192)
FGCOLOR = (0,0,192)
ONCOLOR = (0, 255, 0)
OFFCOLOR= (255,0,0)
SZ = 16

mX_AXIS = 0
mY_AXIS = 1

class jsview(object):
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH,HEIGHT),0,BPP)

    pygame.display.update()
    self.font = pygame.font.Font(None,FONT_SIZE)

    self.xaxis = 0
    self.yaxis = 0
    self.buttons = []

    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
      pygame.joystick.Joystick(i).init()

  def display(self):
    self.screen.fill(BGCOLOR)
    x = 0
    y = 0
    disp = self.font.render("X=%d" % self.xaxis, True, FGCOLOR)
    self.screen.blit(disp,[x,y])
    dims = disp.get_bounding_rect()
    y += dims[3]*1.5

    disp = self.font.render("Y=%d" % self.yaxis, True, FGCOLOR)
    self.screen.blit(disp,[x,y])
    dims = disp.get_bounding_rect()
    y += dims[3]*1.5
 
    dims = [0, y, SZ, SZ]

    for i in self.buttons:
      if (i == 0):
        pygame.draw.rect(self.screen, OFFCOLOR, dims)
      elif (i == -1):
        pygame.draw.rect(self.screen, BGCOLOR, dims)
      else:
        pygame.draw.rect(self.screen, ONCOLOR, dims)
      dims[0] += SZ


    pygame.display.update()

  def assign_button(self,index,value):
    while (index >= len(self.buttons)):
      self.buttons.append(-1)
    self.buttons[index] = value

  def run(self):
    self.display()
    running = True
    while running:
      for event in pygame.event.get():
        if (event.type is JOYAXISMOTION):
          if event.axis == mX_AXIS:
            self.xaxis = event.value
          elif event.axis == mY_AXIS:
            self.yaxis = event.value
          self.display()
        elif (event.type is JOYBUTTONDOWN):
          self.assign_button(event.button,1)
          self.display()
        elif (event.type is JOYBUTTONUP):
          self.assign_button(event.button,0)
          self.display()
        elif (event.type is KEYDOWN):
          if (event.key == K_ESCAPE):
            running = False

if __name__ == "__main__":
  app = jsview()
  app.run()
