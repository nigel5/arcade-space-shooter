import pygame

class Instructions(pygame.sprite.Sprite):
    """This class defines an Instructions label sprite which inherits from pygame.sprite.Sprite."""
    def __init__(self, screen):
        """This method initializes the Instructions label sprite.
                Arguments:
                    screen: the pygame screen object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./Sprite/instructions.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.__screen = screen