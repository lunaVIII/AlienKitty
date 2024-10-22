import pygame

class Settings():
    """A class to store all the settings for Alien Kitty"""

    def __init__(self):
        """Initialize the game's settings"""
        self.game_over = False

        # Screen settings
        self.screen_width = 900
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Margin settings
        self.margin = 20  # Margin for all game elements

        # Outer border settings
        self.outer_border_color = (183, 34, 108)  # Outer border color (Magenta)
        self.outer_border_thickness = 10  # Thickness of the outer border

        # Inner border settings
        self.inner_border_color = (38, 55, 120)  # Inner border color (Nebula Blue)
        self.inner_border_thickness = 8  # Thickness of the inner border

        # Gradient Settings
        self.gradient_start_color = (25, 25, 112)   # Midnight Blue
        self.gradient_end_color = (0, 0, 0)         # Black

        # Kitty settings
        self.kitty_speed = 2.5

        # Bullet settings
        self.bullet_speed = 4.0
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = (255, 248, 231)         # Cosmic latte
        self.bullets_allowed = 3

        # Octo settings
        self.boss_alien_size = (400, 400)
        self.small_alien_size = (100, 100)

        # Health settings (Octo)
        self.max_boss_health = 30
        self.boss_health_bar_length = 600
        self.boss_health_bar_height = 15
        self.max_minion_health = 5
        self.minion_health_bar_length = 50
        self.minion_health_bar_height = 5

        # Health settings (Kitty)
        self.max_kitty_health = 3
        
        # Projectile settings
        self.projectile_speed = 1.5
        self.projectile_color = (255, 0, 0)    
        self.projectile_size = 10

        # Music settings
        self.bullet_sound = pygame.mixer.Sound('alien_invasion/sounds/bullet.wav')
        self.blast_sound = pygame.mixer.Sound('alien_invasion/sounds/blast.wav')
        self.kitty_sound = pygame.mixer.Sound('alien_invasion/sounds/Meow.wav')