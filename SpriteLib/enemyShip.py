import pygame
import random
from playerShip import PlayerShip

class EnemyShip(PlayerShip):
    """This class defines an EnemyShip sprite that inherits from PlayerShip."""
    def __init__(self, screen):
        """
        This method is automatically called when creating an instance of this class.
        It starts the EnemyShip at a random side of the screen, and sets it direction.
        Arguments:
            screen: the pygame screen object
        """        
        PlayerShip.__init__(self, screen)
        self.__screen = screen
        self.__health = 100
        self.__value = 0
        self.reset()
        # New explosion sound for EnemyShip
        self.set_explosion_sound(pygame.mixer.Sound("./Sound/explosion1.wav"))
        self.get_explosion_sound().set_volume(0.5)
        self.__explosions = self.get_explosions()

    def reverse_direction(self):
        """Reverses the direction of the EnemyShip. Does not return anything."""
        self.move((-self.get_dx(), -self.get_dy()))
    
    def get_value(self):
        """Returns the point value of the ship."""
        return self.__value
    
    def get_health_points(self):
        """Returns an integer value of the EnemyShip's health points."""
        return self.__health
    
    def decrease_health_points(self, reduction):
        """Decreases the health of the EnemyShip by the passed in integer value > 0. Does not return anything."""
        if reduction > 0:
            self.__health -= reduction

    def increase_health_points(self, increment):
        """Increases the health of the EnemyShip by the passed in integer value > 0. Does not return anything."""
        if increment > 0:
            self.__health += increment

    def reset(self):
        """Resets the attributes of the EnemyShip. Does not return anything."""
        # Big UFO
        if random.randint(1, 250) == 42:
            self.__value = 500
            self.__health = 5000

            self.image = pygame.image.load("./Sprite/Enemy/ufo.png").convert_alpha()
            self.__image_original = self.image
            self.rect = self.image.get_rect()
            self.rect.center = (0, 0)

            self.set_bullet_damage(225)
            self.move((1, 1))
        else:
            randomNumber = random.randint(1, 4)
            if randomNumber == 1:
                # EnemyShip moving up, starting from bottom
                self.__value = 1
                self.__health = 100

                self.image = pygame.image.load("./Sprite/Enemy/" + str(randomNumber) + ".png").convert_alpha()
                self.image = pygame.transform.rotate(self.image, 90)
                self.__image_original = self.image
                self.rect = self.image.get_rect()
                self.rect.bottom = self.__screen.get_height() + 50
                self.rect.centerx = random.randint(45, self.__screen.get_width() - 45)

                self.set_bullet_damage(5)
                self.move((0, -random.randint(1, 5)))

            elif randomNumber == 2:
                # EnemyShip moving down, starting from top
                self.__value = 2
                self.__health = 75

                self.image = pygame.image.load("./Sprite/Enemy/" + str(randomNumber) + ".png").convert_alpha()
                self.image = pygame.transform.rotate(self.image, -90)
                self.__image_original = self.image
                self.rect = self.image.get_rect()
                self.rect.top = -50
                self.rect.centerx = random.randint(45, self.__screen.get_width() - 45)

                self.set_bullet_damage(20)
                self.move((0, random.randint(1, 4)))

            elif randomNumber == 3:
                # EnemyShip moving right, starting from left
                self.__value = 3
                self.__health = 500

                self.image = pygame.image.load("./Sprite/Enemy/" + str(randomNumber) + ".png").convert_alpha()
                self.__image_original = self.image
                self.rect = self.image.get_rect()
                self.rect.left = -50
                self.rect.centery = random.randint(82, self.__screen.get_height() - 82)

                self.set_bullet_damage(30)
                self.move((random.randint(1, 4), 0))

            else:
                # EnemyShip moving left, starting from right side
                self.__value = 4
                self.__health = 150

                self.image = pygame.image.load("./Sprite/Enemy/" + str(randomNumber) + ".png")
                self.image = pygame.transform.rotate(self.image, 180).convert_alpha()
                self.__image_original = self.image
                self.rect = self.image.get_rect()
                self.rect.right = self.__screen.get_width() + 50
                self.rect.centery = random.randint(82, self.__screen.get_height() - 82)

                self.set_bullet_damage(10)
                self.move((-random.randint(1, 4), 0))

    def update(self):
        """This method updates the location of the EnemyShip, and resets it if it goes off the screen."""
        if self.get_explode():
            # Ship is disabled while exploding
            self.move((0, 0))
            lastloc = self.rect.center
            if self.get_explosion_index() >= 28:
                self.image = self.__image_original
                self.set_explosion_index(0)
                self.set_explode(False)
                self.reset()
            else:
                self.image = self.__explosions[self.get_explosion_index()]
                self.rect = self.image.get_rect()
                self.rect.center = lastloc
                self.set_explosion_index(self.get_explosion_index() + 1)
        else:
            self.rect.centerx += self.get_dx()
            self.rect.centery += self.get_dy()

        if self.rect.left <= -225 or self.rect.right >= self.__screen.get_width() + 225 or \
           self.rect.top <= -225 or self.rect.bottom >= self.__screen.get_height() + 225:
            self.reset()