import pygame
class Button:
      def __init__(self,ai_game,msg):
          self.screen = ai_game.screen
          self.screen_rect = self.screen.get_rect()
          #按钮的尺寸颜色
          self.width,self.height = 200, 50
          self.button_colour = (0,255,0)
          self.text_colour = (255,255,255)
          self.font = pygame.font.SysFont(None,48)  #默认字体 字号48
          #创建按钮的rect选项使其居中
          self.rect = pygame.Rect(0,0,self.width,self.height)
          self.rect.center = self.screen_rect.center
          #按钮标签只需要创建一次
          self._prep_msg(msg)        #显示按钮文本   

      def _prep_msg(self,msg):
          self.msg_image = self.font.render(msg,True,self.text_colour, self.button_colour)  #true的是抗锯齿
          self.msg_image_rect = self.msg_image.get_rect()  #取得文本的矩形  字号大小取决
          self.msg_image_rect.center = self.rect.center    #让文本显示再中间

      def draw_button(self):
          self.screen.fill(self.button_colour,self.rect)
          self.screen.blit(self.msg_image,self.msg_image_rect)                             


