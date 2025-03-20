import sys

import pygame

class AlienInvasion:
    """Manage assets and behavior"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
    
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
        
    def run_game(self):
        """Game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
        
if __name__ == '__main__':
    # Run game instance
    ai = AlienInvasion()
    ai.run_game()
    