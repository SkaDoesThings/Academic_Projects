import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Manage assets and behavior"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)        
        
    def run_game(self):
        """Game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        
            # Redraw screen during each loop pass
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
        
            # Draw most recent screen
            pygame.display.flip()
        
if __name__ == '__main__':
    # Run game instance
    ai = AlienInvasion()
    ai.run_game()
    