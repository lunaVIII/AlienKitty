import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired by kitty"""

    def __init__(self, ak_game):
        """Create a bullet object at kittys current position"""
        super().__init__()
        self.screen = ak_game.screen
        self.settings = ak_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rectangle at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ak_game.kitty.rect.midtop

        # Store the kittys position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Update bullet position and check for boundaries"""
        self.y -= self.settings.bullet_speed 
        if self.rect.y <= self.settings.margin + self.settings.outer_border_thickness + 2 * self.settings.inner_border_thickness:
            self.kill()  # Remove bullet if it goes above the top margin
        else:
            self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)