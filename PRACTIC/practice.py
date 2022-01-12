import pygame
import sys
from setting import Setting
from fling import Ship

class The_pygame:
     pygame.init()
     def __init__(self):
         self.settings = Setting()
         self.screen = pygame.display.set_mode((self.settings.width , self.settings.height))
         pygame.display.set_caption('PRACTICE')
         self.ship = Ship(self)

     def run_game(self):
         while True:
               for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                    sys.exit()    
               self.update_screen()                         

     def update_screen(self):
         self.screen.fill(self.settings.bg_colour)
         self.ship.blitme() 
         pygame.display.flip()
                       
if __name__ == '__main__':
   A=The_pygame()
   A.run_game()                                                                    