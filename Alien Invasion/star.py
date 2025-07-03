import pygame
import random
from pygame.sprite import Sprite


class Star(Sprite):
    """Class to initialize a single star."""
    def __init__(self, ai_game):
        """Initialize star"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the star image and set its rect attribute.
        self.rect = pygame.Rect(0, 0,
                                self.settings.star_width,
                                self.settings. star_height)
        self.rect.x = random.randint(0, self.settings.screen_width -
                                    self.rect.width)
        self.rect.y = random.randint(-self.settings.screen_height +
                                     self.rect.height, 0)


        # Store the stars exact vertical position
        self.y = float(self.rect.y)

    def update(self):
        """Move the star downward."""
        self.y += self.settings.star_speed
        self.rect.y = int(self.y)

    def draw_star(self):
        """Draw star"""
        pygame.draw.rect(self.screen, self.settings.star_color, self.rect)