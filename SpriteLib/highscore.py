import pygame

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