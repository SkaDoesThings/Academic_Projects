class GameStats:
    def __init__(self, game):
        # Start game in active state
        self.game_active = True
    
        self.settings = game.settings
        self.reset_stats()
        
    def reset_stats(self):
        self.lives_left = self.settings.ship_lives