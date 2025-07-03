class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (4,10,46)
        # Ship setting
        self.ship_speed = 1.5
        # Bullet settings
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 102, 102)
        self.bullets_allowed = 3
        self.star_speed = 0.7
        self.star_width = 3
        self.star_height = 3
        self.star_color = (255, 255, 255)
