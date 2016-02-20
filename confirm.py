import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
      return key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   (10,(screen.get_height() / 2) - 40,
                    screen.get_width()-40,80), 0)
  pygame.draw.rect(screen, (255,255,255),
                   (8,(screen.get_height() / 2) - 42,
                    screen.get_width()-16,84),1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                (15, (screen.get_height() / 2) - 30))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  display_box(screen, question)

  while 1:
    inkey = get_key()
    if inkey == K_RETURN or inkey == K_y:
      return True
    elif inkey == K_ESCAPE or inkey == K_n:
      return False

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name")

if __name__ == '__main__': main()
