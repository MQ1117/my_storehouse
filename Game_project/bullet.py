import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
      def __init__(self,ai_game):
          super().__init__()
          self.screen = ai_game.screen
          self.setting = ai_game.settings
          self.colour = self.setting.bullet_colour
          #创建一个子弹的矩形
          self.rect = pygame.Rect(0,0,self.setting.bullet_width,
                  self.setting.bullet_height)
          self.rect.midtop = ai_game.ship.rect.midtop    #飞船矩形的顶部 
          self.y = float(self.rect.y)
          
      def update(self):
          self.y -= self.setting.bullet_speed           #子弹向上飞行 原点（0，0）位于左上角
          self.rect.y = self.y

      def draw_bullet(self):
          pygame.draw.rect(self.screen,self.colour,self.rect)   #绘制子弹                                 
