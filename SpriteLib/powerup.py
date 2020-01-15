import pygame
import random

class Powerup(pygame.sprite.Sprite):
    """This class defines a powerup sprite that keeps can provide various buffs to the player."""
    def __init__(self, screen, powerup_type):
        """Initializes the Powerup Class.
           Arguments:
           screen: the pygame screen object
           powerup_type: an integer representing the powerup type
                        1: Health Points
                        2: Shield Points
                        3: Bullet Damage
        """
        pygame.sprite.Sprite.__init__(self)

        if powerup_type == 1:
            self.image = pygame.image.load("./Sprite/Powerup/crateRepair.png")
            self.rect = self.image.get_rect()
        elif powerup_type == 2:
            self.image = pygame.image.load("./Sprite/Powerup/crateArmor.png")
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.image.load("./Sprite/Powerup/crateAmmo.png")
            self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(1, screen.get_width())
        self.rect.centery = random.randint(1, screen.get_height())
        
        self.__screen = screen
        self.__type = powerup_type
        self.__powerup = powerup_type

    def get_type(self):
        """Returns the powerup type integer."""
        return self.__powerup