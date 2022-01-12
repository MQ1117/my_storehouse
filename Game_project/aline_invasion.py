import sys
from time import sleep  
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scorebord

class AlineInvasion:
      def __init__(self):
       #初始化                        
          pygame.init()
          self.settings=Settings()
          self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))#创建背景   pygame.FULLSCREEN全屏  尺寸可直接导入 但是是要元组
         #  self.settings.screen_width = self.screen.get_rect().width
         #  self.settings.screen_height = self.screen.get_rect().height   #使用屏幕的尺寸
          pygame.display.set_caption('Aline Invasion')#设置标题
          self.stats = GameStats(self)
          self.sb = Scorebord(self)
          self.ship=Ship(self)  #先定义玩背景才能使用
          self.bullet=pygame.sprite.Group()  #存储子弹的编组 类似列表
          self.aliens=pygame.sprite.Group()  #创建外星人的精灵库
          self._create_fleet()
          self.play_button = Button(self,'play')
      def run_game (self):
       #开始游戏循环                 
          while True: #简化run_game函数    
                self._check_events()
                if self.stats.game_active == True:    
                  self.ship.update()
                  self._update_aliens()
                  self._update_bullet()  #更新子弹位置
                self._update_scrren() 

      def _check_events(self): #检测动作     
          for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   sys.exit()
                elif event.type == pygame.KEYDOWN:
                   self._check_keydown_events(event)                               
                elif event.type == pygame.KEYUP:
                   self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                   mouse_pos = pygame.mouse.get_pos() #get_pos可以返回一个元组鼠标点击时的坐标（x，y） 
                   self._check_play_button(mouse_pos)    

      def _check_keydown_events(self,event):          #摁下动作
          if event.key == pygame.K_RIGHT:
             self.ship.moving_right = True
          elif event.key == pygame.K_LEFT:
             self.ship.moving_left = True
          elif event.key == pygame.K_SPACE:
             self._fire_bullet()          

      def _check_keyup_events(self,event):           #弹开动作
          if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
          elif event.key == pygame.K_LEFT:
             self.ship.moving_left = False
          elif event.key == pygame.K_ESCAPE:
               sys.exit()

      def _check_play_button(self,mouse_pos):
          button_clicked = self.play_button.rect.collidepoint(mouse_pos) #鼠标坐标再按钮内就开始
          if button_clicked and  self.stats.game_active == False:
             self.settings.initialize_dynamic_settings()  #重置游戏速度设置
             self.stats.reset_stats()
             self.stats.game_active = True
             self.sb.prep_score()
             self.sb.prep_level()  #调用等级 
             self.sb.prep_ships()
             #清除余下的外星人和子弹
             self.aliens.empty()
             self.bullet.empty()
             #创建一群新的外星人 并让飞船居中
             self._create_fleet()
             self.ship.center_ship()
             pygame.mouse.set_visible(False)         #隐藏鼠标
 
      def _fire_bullet(self):
          new_bullet=Bullet(self)    #创建一颗子弹 加入编组bullet中  
          self.bullet.add(new_bullet)   

      def _create_fleet(self):       #创建外星人群
          alien = Alien(self)
          alien_width,alien_height = alien.rect.size   #size属性相当于元组 包含了width 和 height
          available_space_x = self.settings.screen_width - (2 * alien_width) #外星人之间间距 
          number_alien_x = available_space_x // (2 * alien_width)            #可形成多少外星人
          ship_height = self.ship.rect.height
          available_space_y = (self.settings.screen_height - 
                                    (3 * alien_height) - ship_height)
          number_rows = available_space_y // (2 * alien_height)
          for row_number in range(number_rows):                  #循环判断第几行
              for alien_number in range(number_alien_x):         #一行有几个
                  self._create_alien(alien_number,row_number)  

      def _create_alien(self,alien_number,row_number):          #外星人数量
         alien = Alien(self)
         alien_width,alien_height = alien.rect.size                                         
         alien.x = alien_width + 2 * alien_width * alien_number
         alien.rect.x = alien.x                                        #每个外星人显示的x坐标
         alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
         self.aliens.add(alien)

      def _check_fleet_edges(self):
         for alien in self.aliens.sprites():   #判断是否到达边缘
             if alien.check_edges():
                 self._change_fleet_direction()
                 break

      def _change_fleet_direction(self):
          for alien in self.aliens.sprites():     #到达边缘后往下十个像素点再反方向移动
              alien.rect.y += self.settings.fleet_drop_speed
          self.settings.fleet_direction *= -1   

      def _check_aliens_bottom(self):
          screen_rect = self.screen.get_rect()
          for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                  self._ship_hit()   #撞到底部就像撞到飞船一样处理
                  break                   

      def _update_bullet(self):
          self.bullet.update()
          for bullet in self.bullet.copy():   #子弹元组副本
              if bullet.rect.bottom < 0:      #子弹底部到达顶部
                 self.bullet.remove(bullet) #删除子弹s
          self._check_bullet_alien_collisions() 

      def _check_bullet_alien_collisions(self):
         #比较子弹和外星人是否碰撞并返回一个字典 如果碰撞 则返回一个值对 key为子弹 值为外星人 
          collisions =  pygame.sprite.groupcollide(self.bullet,self.aliens,True,True) 
          if collisions:
             for aliens in collisions.values():   #返回字典里的所有的值
                 self.stats.score += self.settings.alien_points * len(aliens)  #击落一个外星人就得分，如果一颗子弹击中两个也算一个的分数
                 self.sb.prep_score()                  #数字显示成文本图像
                 self.sb.check_hight_score()
          if not self.aliens: 
             self.bullet.empty()
             self._create_fleet()       #如果外星人都没了 清除界面上的子弹 新建一波外星人 
             self.bullet.empty()       #如果外星人都杀完了 加速增加难度
             self._create_fleet()
             self.settings.increase_speed()
             self.stats.level += 1
             self.sb.prep_level()   

      def _ship_hit(self):
          if self.stats.ship_life > 0:
          #飞船左部扣一
             self.stats.ship_life -= 1
             self.sb.prep_ships()
          #清空外星人和子弹
             self.aliens.empty()
             self.bullet.empty()
          #创建新的一群外星人，并将飞船放在底部中央
             self._create_fleet()
             self.ship.center_ship()
          #暂停0.5s
             sleep(0.5)
          else:
              self.stats.game_active = False   #  如果玩家飞船没了就游戏结束
              pygame.mouse.set_visible(True)      #显示鼠标       
         
      def _update_aliens(self):
          self.aliens.update()
          if pygame.sprite.spritecollideany(self.ship,self.aliens): #两个实参 一个精灵组一个编组
             self._ship_hit()
          self._check_fleet_edges()
          self._check_aliens_bottom()  #检测外星人是否在底部           

      def _update_scrren(self):   #不断更新                                                    
                self.screen.fill(self.settings.bg_colour)#每次刷新背景   fill填充 
                self.ship.blitme()
                for bullet in self.bullet.sprites():
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
                self.sb.show_score()
                if not self.stats.game_active:
                   self.play_button.draw_button()                     
                pygame.display.flip()         #展示最新的一页                                                                      

if __name__=='__main__':
   ai=AlineInvasion()
   ai.run_game()               

