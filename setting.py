class Settings:
    def __init__(self):
        #初始化设置
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        #子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1表示向右移动，-1表示向左移动
        self.ship_limit = 0  #飞船数量