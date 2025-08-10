import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats

class AlienInvasion:
    #创建对象时会自动调用一次 属于类的构造函数
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # 创建一个子弹编组
        self.aliens = pygame.sprite.Group()  # 创建一个外星人编组
        self._create_fleet()  # 创建外星人舰队
        self.stats = GameStats(self)  # 创建游戏统计信息实例
    # class AlienInvasion:
    #     def __init__(self):
    #         settings = Settings()        # 普通变量，只在 __init__ 这个函数里能用
    #         self.settings = Settings()   # 实例属性，整个对象中都能用
    #
    #     def run_game(self):
    #         print(self.settings.bg_color)  # ✅ 正确，self.settings 可以访问
    #         # print(settings.bg_color)     # ❌ 报错，这里访问不到 settings

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_screen()
                self._update_bullets()
            else:
                print("Game Over")
                print("有点可惜啊，再来一次吧！")
                print("空格发射，⬅➡左右移动，先射杀底下的外星人会更容易获得胜利")
                sys.exit()
            self._update_aliens()


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        #检查子弹和外星人之间的碰撞
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 如果外星人全灭

        if not self.aliens:

            #播放音效
            pygame.mixer.music.load("images/111246643-1-208_1.mp3")
            pygame.mixer.music.play()

            # 显示胜利图片
            win_image = pygame.image.load("images/Snipaste_2025-08-10_18-41-24.png ")
            win_rect = win_image.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(win_image, win_rect)
            pygame.display.flip()

            # # 暂停几秒
            # pygame.time.delay(3000)
            # pygame.quit()
            # sys.exit()

    #实例方法的第一个参数必须是self,只有有了它，方法内部才能访问实例属性和其他方法。
    def _check_events(self):
        #响应鼠标按键
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         #向右移动
            #         # self.ship.rect.x += 1
            #         self.ship.moving_right = True
            #     elif event.key == pygame.K_LEFT:
            #         #向左移动
            #         # self.ship.rect.x -= 1
            #         self.ship.moving_left = True
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_RIGHT:
            #         #停止向右移动
            #         # self.ship.rect.x -= 1
            #         self.ship.moving_right = False
            #     elif event.key == pygame.K_LEFT:
            #         self.ship.moving_left = False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键按下事件"""
        if event.key == pygame.K_RIGHT:
            #向右移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #向左移动
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开事件"""
        if event.key == pygame.K_RIGHT:
            #停止向右移动
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹并将其加入编组"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        # 每次循环都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # 绘制飞船
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 绘制外星人
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _create_fleet(self):
        """创建外星人舰队"""
        # 创建一个外星人并计算一行可以容纳多少个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _update_aliens(self):
        """检查外星人是否到达屏幕边缘，并更新位置"""
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship hit!!!")
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        """响应外星人到达屏幕边缘"""
        # 检查是否有外星人到达屏幕边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到的情况"""
        if self.stats.ships_left > 0:
            #将ships_left减1
            self.stats.ships_left -= 1
            #清空外星人和子弹列表
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人，并将飞船放到屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()
            #暂停一会儿
            sleep(0.5)
        else:
            self.stats.game_active = False
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #如果有外星人到达屏幕底部，就调用_ship_hit方法
                self._ship_hit()
                break

#只有运行该文件时，才会进行以下行为
#（）内定义时要写，但调用时不用写，调用时会自动传入ai
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()



