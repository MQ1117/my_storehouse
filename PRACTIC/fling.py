import pygame
class Ship:
     def __init__(self,A_game):
         self.screen = A_game.screen  
         self.screen_rect = self.screen.get_rect()
         self.image = pygame.image.load("PRACTIC\picture\ship.jpg")
         self.image_rect = self.image.get_rect()
         self.image_rect.midbottom = self.screen_rect.midbottom 

     def blitme(self):
         self.screen.blit(self.image , self.image_rect)
                       