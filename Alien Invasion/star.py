import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """Class to initialize a single star."""
    def __init__(self, ai_game):
        """Initialize star"""
        super().__init__()

        self.screen = ai_game.screen

        # Load the star image and set its rect attribute.
        self.og_image = pygame.image.load('images/star-'
                                          'png-transparent-image-pngpix-5.png')
        self.image = pygame.transform.scale(self.og_image, (25,25))
        self.rect = self.image.get_rect()

        # Start each new star near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the stars exact vertical position
        self.y = float(self.rect.y)