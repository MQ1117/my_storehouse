import pygame.font
from pygame.sprite import Group, Sprite
from ship import Ship

class Scorebord:
      def __init__(self,ai_game):
          self.ai_game = ai_game
          self.screen = ai_game.screen
          self.settings = ai_game.settings
          self.screen_rect = self.screen.get_rect()
          self.stats = ai_game.stats
          self.text_colour = (30,30,30)
          self.font = pygame.font.SysFont(None,48)
          self.prep_score()
          self.prep_hight_score()
          self.prep_level()
          self.prep_ships() 

      def prep_score(self):
          score_str = str(self.stats.score)  #转换为字符串
          rounded_score = round(self.stats.score, -1)   #舍入成最近的十的倍数
          score_str="{:,}".format(rounded_score)    #插入逗号
          self.score_image = self.font.render(score_str,True,
               self.text_colour,self.settings.bg_colour)      #将得到的字符串转换为图像
          self.score_rect = self.score_image.get_rect()
          self.score_rect.right = self.screen_rect.right - 20
          self.score_rect.top = 20                             #距离画框上下都20像素点     

      def prep_hight_score(self):
          hight_score = round(self.stats.hight_score, -1)
          hight_score_str = "{:,}".format(hight_score)
          self.hight_score_image = self.font.render(hight_score_str,True,
               self.text_colour,self.settings.bg_colour)
            #最高分数放在顶部中央
          self.hight_screen_rect = self.hight_score_image.get_rect()
          self.hight_screen_rect.centerx = self.screen_rect.centerx
          self.hight_screen_rect.top = self.screen_rect.top

      def prep_level(self):
          level_str = str(self.stats.level)
          self.level_image = self.font.render(level_str,True,
               self.text_colour,self.settings.bg_colour)
            #设置等级放在得分下面
          self.level_rect = self.level_image.get_rect()
          self.level_rect.top = self.score_rect.bottom +10
          self.level_rect.right = self.score_rect.right

      def prep_ships(self):
          self.ships = Group()
          for ship_number in range(self.stats.ship_life):
              ship = Ship(self.ai_game)
              ship.rect.x = 10 + ship_number * ship.rect.width
              ship.rect.y = 10
              self.ships.add(ship)          

      def check_hight_score(self):
          if self.stats.score > self.stats.hight_score:
             self.stats.hight_score = self.stats.score
             self.prep_hight_score()     


      def show_score(self):
          self.screen.blit(self.score_image,self.score_rect) 
          self.screen.blit(self.hight_score_image,self.hight_screen_rect) 
          self.screen.blit(self.level_image,self.level_rect) 
          self.ships.draw(self.screen)                           