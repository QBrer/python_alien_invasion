import sys
import pygame
from setting import Settings
from ship import Ship
class AlienInvasion:
    #创建对象时会自动调用一次 属于类的构造函数
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
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
            self.ship.update()
            self._update_screen()

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

    def _check_keyup_events(self, event):
        """响应按键松开事件"""
        if event.key == pygame.K_RIGHT:
            #停止向右移动
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        # 每次循环都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # 绘制飞船
        # 让最近绘制的屏幕可见
        pygame.display.flip()

#只有运行该文件时，才会进行以下行为
#（）内定义时要写，但调用时不用写，调用时会自动传入ai
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()



