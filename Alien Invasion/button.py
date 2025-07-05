import pygame.font

class Button:
    def __init__(self, ai_game, msg, x, y, color_bg, color_text):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200,50
        self.button_color = color_bg
        self.text_color = color_text
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it at x and y.
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.rect.center = (x,y)
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """Turn into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


