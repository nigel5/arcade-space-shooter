import pygame

class Lifekeeper(pygame.sprite.Sprite):
    """This class defines a label sprite that keeps track of health, and shield points."""
    def __init__(self, screen):
        """This method initializes the Lifekeeper sprite with the screen object.
           Arguments:
               screen: the pygame screen object
        """
        pygame.sprite.Sprite.__init__(self)

        self.__health = 500
        self.__shield = 0
        
        self.__screen = screen
        self.__message = ""
        self.__font = pygame.font.Font("./Font/kenvector_future.ttf", 30)

    def take_damage(self, damage):
        """Causes the Lifekeeper to take damage, first on the shield. If no shield, then the health will take damage."""
        if self.__shield - damage >= 0:
            self.__shield -= damage
        elif self.__shield - damage < 0:
            remainder = -(self.__shield - damage)
            self.__shield -= damage - remainder
            self.__health -= remainder

    def get_shield_points(self):
        """Returns an integer value of the ship's shield points."""
        return self.__shield

    def increase_shield_points(self, increment):
        """Increases the shield points of the ship by the passed in integer value > 0."""
        if increment > 0:
            self.__shield += increment
    
    def get_health_points(self):
        """Returns an integer value of the ship's health points."""
        return self.__health
        
    def increase_health_points(self, increment):
        """Decreases the health of the ship by the passed in integer value > 0."""
        if increment > 0:
            self.__health += increment
        
    def update(self):
        """This is the update function that is called automatically by pygame. It renders the score onto the screen"""
        if self.__health <= 0:
            self.__message = "0    " + str(self.__shield)
        else:
            self.__message = "HEALTH " + str(self.__health) + "    " + "SHIELD " + str(self.__shield)
            
        self.image = self.__font.render(self.__message, 1, (0, 206, 209))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width() / 2
        self.rect.centery = 30