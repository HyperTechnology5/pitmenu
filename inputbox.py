# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key (FIXED)
# And, for reasons of my own, this program converts "-" to "_" (REMOVED)

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

SHIFTS = {
  K_0: ')',
  K_1: '!',
  K_2: '@',
  K_3: '#',
  K_4: '$',
  K_5: '%',
  K_6: '^',
  K_7: '&',
  K_8: '*',
  K_9: '(',
  K_BACKQUOTE: '~',
  K_MINUS: '_',
  K_EQUALS: '+',
  K_LEFTBRACKET: '{',
  K_RIGHTBRACKET: '}',
  K_BACKSLASH: '|',
  K_SEMICOLON: ':',
  K_QUOTE: '"',
  K_COMMA: '<',
  K_PERIOD: '>',
  K_SLASH: '?',
};

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      key = event.key
      if (K_a <= key and key <= K_z and ((event.mod & (KMOD_CAPS|KMOD_SHIFT)))):
        key = key - K_a + 65
      elif (event.mod & KMOD_SHIFT):
        if key in SHIFTS:
          key = ord(SHIFTS[key])

      return key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   (10,(screen.get_height() / 2) - 10,
                    screen.get_width()-20,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   (8,(screen.get_height() / 2) - 12,
                    screen.get_width()-16,24),1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                (15, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question, value=""):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  for i in range(len(value)):
    current_string.append(value[i])
  display_box(screen, question + ": " + string.join(current_string,""))

  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      if (pygame.key.get_mods() & KMOD_CTRL):
        current_string = []
      else:
        current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_ESCAPE:
      return None

    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name","alex") + " was entered"

if __name__ == '__main__': main()
