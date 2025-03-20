class Settings:
    """Stores all settings for Alien Invasion"""
    
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 225, 225)
        
        # Ship settings
        self.ship_speed = 1.5
        self.max_bullets = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)