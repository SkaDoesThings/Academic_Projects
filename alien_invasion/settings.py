class Settings:
    """Stores all settings for Alien Invasion"""
    
    def __init__(self):
        """Initialize static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 225, 225)
        
        # Ship settings
        self.max_bullets = 3
        self.ship_lives = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        
        # Alien settings
        self.fleet_drop_speed = 10
        
        # Scale settings
        self.speedup_scale = 1.1
        self.scoring_scale = 1.5 
        self.dynamic_settings()
        
    def dynamic_settings(self):
        """Initialize dynamic settings"""
        # Game speeds
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 0.1
        
        # Values
        self.alien_points = 50
        
        # Value of 1 is right, -1 is left
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and point values"""
        # Increase speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # Increase point scale
        self.alien_points = int(self.alien_points * self.scoring_scale)