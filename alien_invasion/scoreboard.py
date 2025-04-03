import pygame.font

class Scoreboard:
    """Class to report scoring information"""
    
    def __init__(self, game):
        """Initialize scorekeeping attributes"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        
        # Font settings
        self.text_color = (35, 35, 35)
        self.font = pygame.font.SysFont(None, 48)
        
        # Prepare initial score image
        self.prepare_score()
        self.prepare_high_score()
        self.prepare_level()
        
    def prepare_score(self):
        """Turn score into an image"""
        rounded_score = round(self.stats.score, -1)
        score_text = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_text, True, self.text_color, self.settings.bg_color)
        
        # Display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prepare_high_score(self):
        """Turn high score into rendered image"""
        high_score = round(self.stats.high_score, -1)
        score_text = "{:,}".format(high_score)
        self.high_score_image = self.font.render(score_text, True, self.text_color, self.settings.bg_color)
        
        # Display score at top right of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def prepare_level(self):
        """Turn level into rendered image"""
        wave_value = str(self.stats.wave)
        self.wave_image = self.font.render(wave_value, True, self.text_color, self.settings.bg_color)
        
        # Display score at top right of screen
        self.wave_rect = self.wave_image.get_rect()
        self.wave_rect.right = self.screen_rect.right
        self.wave_rect.top = self.score_rect.bottom + 10
        
        
    def check_high_score(self):
        """Check to see if there's a new high score"""
        if (self.stats.score > self.stats.high_score):
            self.stats.high_score = self.stats.score
            self.prepare_high_score()
          
    def show_score(self):
        """Draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.wave_image, self.wave_rect)
