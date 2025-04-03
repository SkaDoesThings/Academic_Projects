class GameStats:
    def __init__(self, game):
        # Start game in active state
        self.game_active = False
    
        self.settings = game.settings
        self.reset_stats()
        
        # Game stats
        self.high_score = 0
        self.wave = 1
        
    def reset_stats(self):
        self.lives_left = self.settings.ship_lives
        self.score = 0