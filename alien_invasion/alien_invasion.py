# Spencer Augenstein
# Alien Invasion Game
# Fun game project that involves shooting down alien ships. Based on Python Crash Course by Eric Matthes
# Created: 3/26/2025 | Updated: 3/20/2025

# Import libraries and local files
import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Manage assets and behavior"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Create game objects
        self.ship = Ship(self)        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # Store and display game statistics
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        
        # Create alien fleet
        self._create_fleet()
        
        # Create play button
        self.play_button = Button(self, "Play Game")
        
    def run_game(self):
        """Main game loop"""
        while True:
            self._check_events()

            if (self.stats.game_active):
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

# -=-=-= ( Check for Keys ) =-=-=- 
          
    def _check_events(self):
        """Check for specific event commands """
        for event in pygame.event.get():
            # Detect if the game should be closed
            if (event.type == pygame.QUIT):
                sys.exit()
            # Detect keypresses
            elif (event.type == pygame.KEYDOWN):
                self._check_keydown_events(event)
            elif (event.type == pygame.KEYUP):
                self._check_keyup_events(event)
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_position = pygame.mouse.get_pos()
                self._check_click_event(mouse_position)

    def _check_click_event(self, mouse_position):
        """React to mouse click events on buttons"""
        # Start game when player clicks play
        if (self.play_button.rect.collidepoint(mouse_position) and not self.stats.game_active):
            # Reset game state
            self.stats.reset_stats()
            self.settings.dynamic_settings()
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            
            # Start game
            self.stats.game_active = True
            
            # Hide mouse cursor
            pygame.mouse.set_visible(False)
        
    def _check_keydown_events(self, event):
        """Detect when keys are pressed"""
        # Ship movement
        if (event.key == pygame.K_LEFT):
            self.ship.moving_left = True
        elif (event.key == pygame.K_RIGHT):
            self.ship.moving_right = True
        # Fire bullets
        elif (event.key == pygame.K_SPACE):
            self._fire_bullet()
        # Quit game
        elif (event.key == pygame.K_q):
            sys.exit()

    def _check_keyup_events(self, event):
        """Stop moving ship when key is released"""
        if (event.key == pygame.K_LEFT):
            self.ship.moving_left = False
        elif (event.key == pygame.K_RIGHT):
            self.ship.moving_right = False

# -=-=-=-=-= ( Bullets ) =-=-=-=-=-

    def _fire_bullet(self):
        # Fire a bullet if bullets are avalible
        if (len(self.bullets) < self.settings.max_bullets):
            spawned_bullet = Bullet(self)
            self.bullets.add(spawned_bullet)
  
# -=-=-= ( Update Components ) =-=-=-
            
    def _update_bullets(self):
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom <= 0):
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
             
    def _update_aliens(self):
        # Check if alien is on an edge
        self._check_fleet_edges()
        # Update position of all aliens
        self.aliens.update()
    
        # Detect when alein hits bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        # Screen properties
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
    
        # Update all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Draw scoreboard value
        self.scoreboard.show_score()
    
        # Draw the play button when game is inactive
        if (not self.stats.game_active):
            self.play_button.draw_button()
        
        # Draw most recent screen
        pygame.display.flip()
        
# -=-=-= ( Manage Aliens ) =-=-=-
    
    def _create_fleet(self):
        # Initialize alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        # Find out how many aliens can be placed based on screen size
        avalible_space_x = self.settings.screen_width - (2 * alien_width)
        aliens_per_row = avalible_space_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        avalible_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        # Changed the variable of 2 -> 1 for the pattern to work
        number_of_rows = avalible_space_y // (1 * alien_height)
        
        # Materialize a row of aliens for each row
        for row_number in range(number_of_rows):
            for alien_number in range(aliens_per_row):
                
                if (self.stats.wave == 1):
                    # Create diagonal patterns by checking if the x and y are equal for each integer on
                    # the grid and a formula to create an inverse diagonal
                    if (alien_number == row_number or alien_number == (aliens_per_row - row_number - 1)):
                        # Divide row_number by 2 to compress the pattern to the top half of the screen
                        self._create_alien((alien_number), (row_number / 2))
                    
            
    def _create_alien(self, alien_number, row_number):
        # Initialize alien
        alien = Alien(self)
    
        # Determine x and y sizes
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
    
        # Officially add the aliens
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # Check if any aliens hit the playfield border
        for alien in self.aliens.sprites():
            if (alien.check_edges()):
                # Drop down and change directions
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Drop aliens down a layer
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # Change alien direction
        self.settings.fleet_direction *= -1
        
    def _check_aliens_bottom(self):
        # Check if aliens hit the bottom playfield border
        for alien in self.aliens.sprites():
            if (alien.rect.bottom >= self.settings.screen_height):
                # Make ship loose a life
                self._ship_hit()
                break
     
# -=-=-= ( Manage Collisions ) =-=-=-       
    
    def _check_bullet_alien_collisions(self):
        """Respond to alien collisions"""
        
        # Check if bullets hit an alien, if so get rid of both
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
                
        # Increase score for all object collisions
        if (collisions):
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.check_high_score()
            
        # Destory existing bullets and create new alien fleet
        if (not self.aliens):
            self.bullets.empty()
            self._create_fleet()        
            # Increase game speed
            self.settings.increase_speed()
            
            # Increase level
            self.stats.wave += 1
            self.scoreboard.prepare_level()
 

    def _ship_hit(self):
        if (self.stats.lives_left > 0):
            # Decrease lives by 1.
            self.stats.lives_left -= 1

            # Get rid of bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Briefly pause
            sleep(0.5)
        else:
            print("!! Game Over !!")
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


# -=-=-=-=-= ( Run Game ) =-=-=-=-=-
    
if (__name__ == '__main__'):
    
    # Run game instance
    alien = AlienInvasion()
    alien.run_game()
    