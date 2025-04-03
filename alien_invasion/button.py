import pygame.font

class Button:
    def __init__(self, game, msg):
        """Initialize button attributes"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set button dimensions and styling
        self.width, self.height = 200, 50
        self.button_color = (255, 120, 120)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Form rectangle object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Prepare button message
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """Turn message into rendered image and center text"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        # Draw blank button then a message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        