import pygame

class Scorekeeper(pygame.sprite.Sprite):
    """This class defines a label sprite that keeps track of score."""
    def __init__(self, screen):
        """This method automatically initializes the Scorekeeper class.
               Arguments:
                   screen: the pygame screen object
        """
        pygame.sprite.Sprite.__init__(self)

        self.__score = 0
        self.__screen = screen
        self.__font = pygame.font.Font("./Font/kenvector_future.ttf", 30)
        
        self.image = self.__font.render(str(self.__score), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 30
        self.rect.centery = 30

    def increase_score(self, increase):
        """Increases the score by the passed in integer > 0."""
        if increase > 0:
            self.__score += increase
    
    def get_score(self):
        """Returns the score (integer)."""
        return self.__score

    def update(self):
        """This is the update function that is called automatically by pygame. It renders the score onto the screen"""
        self.image = self.__font.render(str(self.__score), 1, (255, 255, 255))