"""
    spaceBattleGame sprite module
    (c) 2019 nigel5
"""
import pygame
import math
import random


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


class Powerup(pygame.sprite.Sprite):
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


class Highscore(pygame.sprite.Sprite):
    """This class defines a Highscore label sprite which inherits from pygame.sprite.Sprite."""
    def __init__(self):
        """This method initializes the Highscore label sprite. It accepts no arguments."""
        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./Font/kenvector_future.ttf", 50)

        try:
            self.__scorefile = open("./Data/highscore.txt", "r")
            self.__latest_score = int(self.__scorefile.readline())
            # Only need to read file once
            self.__scorefile.close()
        except IOError:
            self.__latest_score = "N/A"
            print("./Data/highscore.txt could not be opened")
        except ValueError:
            self.__latest_score = "N/A"
            print("./Data/highscore.txt contains corrupt data")

        self.image = self.__font.render(str(self.__latest_score), 1, (255, 168, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 95)

    def get_latest_score(self):
        """Returns the score that is in ./Data/highscore.txt (int)."""
        return self.__latest_score

    def new_highscore(self, score):
        """This class will update the highscore file with the passed in highscore (int)."""
        self.__scorefile = open("./Data/highscore.txt", "w")
        self.__scorefile.write(str(score))
        self.__scorefile.close()

        # Update the rendered font
        self.image = self.__font.render(str(score), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 95)
