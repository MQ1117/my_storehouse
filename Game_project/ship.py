import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
      def __init__(self,ai_game):
          super().__init__()
          #初始化飞船并设置其初始位置
          self.screen = ai_game.screen
          self.screen_rect = ai_game.screen.get_rect()
          self.setting=ai_game.settings   #等于主程序的self.settings

          #加载飞船模型 矩形
          self.image = pygame.image.load('Game_project/images/ship.bmp')
          self.rect = self.image.get_rect()

          #对于每艘新飞船，都放在底部
          self.rect.midbottom = self.screen_rect.midbottom
          self.x=float(self.rect.x)  #rect.x只能存储小数  中转一下
          self.moving_right = False #移动标志
          self.moving_left = False 

      def update(self):               #摁住持续移动
          if self.moving_right and self.rect.right < self.screen_rect.right:  #飞船矩形的右边缘   画框的右边缘
              self.x += self.setting.ship_speed
          elif self.moving_left and self.rect.left > 0:                       #飞船矩形的左边缘
              self.x -= self.setting.ship_speed
          self.rect.x = self.x
                   
      def blitme(self):
          #指定位置绘制飞船
          self.screen.blit(self.image,self.rect)

      def center_ship(self):
          self.rect.midbottom = self.screen_rect.midbottom
          self.x = float(self.rect.x)    
      
