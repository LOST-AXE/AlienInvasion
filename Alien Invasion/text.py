import pygame.font

class Text:
    """Manage the game's text creation and placement."""
    def __init__(self,ai_game, msg, theme, font, y):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont(None, font)
        self.setting_text_dark = (255, 255, 0)
        self.setting_text_light = (0, 0, 0)
        if theme == "Dark":
            self.msg_image = self.font.render(msg, True,
                                              self.setting_text_dark)
        if theme == "Light":
            self.msg_image = self.font.render(msg, True,
                                              self.setting_text_light)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
        self.msg_image_rect.y = y
        self.screen.blit(self.msg_image, self.msg_image_rect)




