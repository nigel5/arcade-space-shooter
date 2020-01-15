import pygame
import math

class Bullet(pygame.sprite.Sprite):
    """This class defines a Bullet sprite that inherits pygame.sprite.Sprite."""
    def __init__(self, screen, originsprite, whoshot, target=None):
        """This method is automatically called when creating an instance of this class to initialize the object
        Arguments:
            screen: the pygame screen object
            originsprite: the origin sprite; the sprite that shoots the bullet
            whoshot: a string for who shot the bullet, used to identify the bullet
            target (optional): Instead of the Bullet moving based on the originsprite angle,
                               it will go directly towards a passed in target sprite.
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./Sprite/bullet.png")     

        self.rect = self.image.get_rect()
        self.rect.center = originsprite.rect.center

        self.__screen = screen
        self.__target = target
        self.__damage = originsprite.get_bullet_damage()
        self.__origin_sprite = originsprite
        self.__who_shot = whoshot
        self.__speed = 25
        self.__direction = self.get_direction()

    def who_shot(self):
        """Returns who shot the Bullet."""
        return self.__who_shot

    def get_direction(self):
        """Calculates and returns a normalized (x, y) direction of the bullet based on the origin, and the ship angle."""

        # Bullets made by the EnemyShip will just go towards the player, no angles.
        if self.__target:
            vx = self.__origin_sprite.rect.centerx - self.__target.rect.centerx
            vy = self.__origin_sprite.rect.centery - self.__target.rect.centery
            mag = math.sqrt(vx ** 2 + vy ** 2) * 1.0

            direction = (-vx / mag, -vy / mag)
            return direction
        else:
            tempAngle = self.__origin_sprite.get_angle()

            # Convert negative angles to positive
            if tempAngle < 0:
                tempAngle += 360

            # Return basic basic directions
            if tempAngle == 90:
                return 0, -1
            elif tempAngle == 180:
                return -1, 0
            elif tempAngle == 270:
                return 0, 1
            elif tempAngle == 0:
                return 1, 0

            # Check which direction the sprite is facing (left or right)
            if 0 <= tempAngle <= 90 or 270 <= tempAngle <= 360:
                tempRay = 1000
            else:
                tempRay = -1000

            # Calculate direction
            vx = tempRay - self.__origin_sprite.rect.centerx
            vy = math.tan(math.radians(tempAngle)) * tempRay

            # Normalize direction
            mag = math.sqrt(vx ** 2 + vy ** 2) * 1.0

            direction = (vx / mag, -vy / mag)
            return direction

    def get_bullet_damage(self):
        """Returns the integer bullet damage value."""
        return self.__damage

    def update(self):
        """This method is automatically called by Pygame. This method updates the position of the bullet towards the
           given direction."""
        # The bullet will destroy itself if it goes off the screen
        if self.rect.left <= 0 or self.rect.right >= self.__screen.get_width() or \
           self.rect.top <= 0 or self.rect.bottom >= self.__screen.get_height():
            self.kill()
            
        self.rect.centerx += self.__direction[0] * self.__speed
        self.rect.centery += self.__direction[1] * self.__speed