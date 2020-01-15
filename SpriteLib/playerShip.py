import pygame

class PlayerShip(pygame.sprite.Sprite):
    """This class defines a PlayerShip sprite that can be controlled by the player.
       This class inherits from pygame.sprite.Sprite."""
    def __init__(self, screen):
        """
        This method is automatically called when creating an instance of this class. It
        centers the ship in the middle of the screen, and sets its default attributes.
        Arguments:
            screen: the pygame screen object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./Sprite/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((320, 240))

        self.__explosions = []
        for count in range(1, 30):
            temp = pygame.image.load(("./Sprite/Explosion/" + str(count) + ".png")).convert_alpha()
            self.__explosions.append(temp)
        self.__explosionSound = pygame.mixer.Sound("./Sound/explosion.wav")
        self.__explosionSound.set_volume(1.0)
        self.__exploding = False

        self.__screen = screen
        self.__image_original = self.image
        self.__speed = 10
        self.__index = 0
        self.__angle = 0
        self.__dx = 0
        self.__dy = 0
        self.__last_pos = self.rect.center
        self.__bullet_damage = 20

    def move(self, direction):
        """Moves the ship in the direction of the passed in tuple (x, y). Does not return anything."""
        self.__dx, self.__dy = direction[0], direction[1]

    def rotate(self, angle):
        """Increases the rotation of the sprite by the given angle (degrees). Does not return anything."""
        self.__last_pos = self.rect.center

        self.__angle += angle
        if self.__angle >= 360 or self.__angle <= -360:
            self.__angle = 0

        # A copy of the original image is used otherwise constant rotations would cause a memory error because
        # pygame creates a new image after each transformation.
        self.image = pygame.transform.rotate(self.__image_original, self.__angle)
        self.rect = self.image.get_rect(center=self.__last_pos)
        
    def explode(self):
        """Makes the ship explode with a sound effect. Does not return anything."""
        self.__index = 0
        self.__exploding = True
        self.__explosionSound.play()

    def get_explode(self):
        """Returns True or False if exploding."""
        return self.__exploding

    def set_explode(self, explode):
        """Set True or False if the ship is exploding."""
        if type(explode) == bool:
            self.__exploding = explode

    def get_explosions(self):
        """Returns a list of the explosion images."""
        return self.__explosions

    def get_explosion_sound(self):
        """Returns the explosion sound."""
        return self.__explosionSound

    def set_explosion_sound(self, sound):
        """Sets the explosion sound to a new pygame.mixer.Sound object."""
        self.__explosionSound = sound

    def get_explosion_index(self):
        """Returns the explosion index."""
        return self.__index

    def set_explosion_index(self, index):
        """Sets the explosion index to the passed in integer."""
        self.__index = index

    def get_speed(self):
        """Returns the speed (int) of the ship."""
        return self.__speed

    def set_speed(self, speed):
        """Sets the speed to the passed in integer value > 0. Does not return anything."""
        if speed > 0:
            self.__speed = speed
        else:
            self.__speed = 1

    def get_bullet_damage(self):
        """Returns the bullet damage value (int) of the ship."""
        return self.__bullet_damage

    def set_bullet_damage(self, damage):
        """Sets the bullet damage of the ship to the passed in integer value > 0. Does not return anything."""
        if damage > 0:
            self.__bullet_damage = damage
        else:
            self.__bullet_damage = 20

    def get_dx(self):
        """Returns X direction."""
        return self.__dx
    
    def get_dy(self):
        """Returns Y direction."""
        return self.__dy
    
    def get_angle(self):
        """Returns the current angle of the ship."""
        return self.__angle
    
    def get_screen(self):
        """Returns the screen object that it has stored in memory."""
        return self.__screen

    def update(self):
        """This method is automatically called by Pygame. It updates the position of the ship,
           and makes it explode if __exploding is True."""
        if self.get_explode():
            lastloc = self.rect.center
            if self.__index >= 28:
                self.__index = 0
                self.__exploding = False
            else:
                self.image = self.__explosions[self.__index]
                self.rect = self.image.get_rect()
                self.rect.center = lastloc
                self.__index += 1
        # Movement
        if self.rect.left < 0:
            self.rect.right = self.__screen.get_width()
        elif self.rect.right > self.__screen.get_width():
            self.rect.left = 0
        elif self.rect.top < 0:
            self.rect.bottom = self.__screen.get_height()
        elif self.rect.bottom > self.__screen.get_height():
            self.rect.top = 0
        else:
            self.rect.centerx += self.get_dx() * self.__speed
            self.rect.centery += self.get_dy() * self.__speed
            self.__dx = 0
            self.__dy = 0