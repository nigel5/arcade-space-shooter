"""
    spaceBattleGame
     Destroy as many enemy spaceships as you can
     Do not collide with enemy spaceships, or you will blow up!
     Collect crates to get boost you spaceship's health, shield, or damage
     (c) 2018 nigel5
"""
# IMPORT AND INITIALIZE
import pygame
import random
import spaceBattleGameSprites

pygame.mixer.init()
pygame.init()


def main():
    """The main function handles the Game <--> Instruction screen loop"""
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("spaceBattleGame 2018")
    new_score = 0
    # Alternates between the game, and the starting screen until the player stops playing
    while True:
        if instructions(screen, new_score):
            new_score = game(screen)
        else:
            break
    pygame.mixer.quit()
    pygame.quit()


def instructions(screen, new_score):
    """This function displays the starting screen, and handles if the player wants to play or quit.
       Returns True if the player wants to play. Returns False if the player wants to quit."""
    # DISPLAY
    screen = screen

    # ENTITIES
    background = pygame.image.load("./Sprite/space.png").convert()
    screen.blit(background, (0, 0))

    instructions_label = spaceBattleGameSprites.Instructions(screen)
    highscore_label = spaceBattleGameSprites.Highscore()
    # Update the score file if new highscore
    if new_score > highscore_label.get_latest_score():
        highscore_label.new_highscore(new_score)

    pygame.mixer.music.load("./Sound/imarch.wav")
    pygame.mixer.music.play(-1)

    # Instantiate 6 ships
    allShips = []
    for ship in range(6):
        allShips.append(spaceBattleGameSprites.EnemyShip(screen))
    allShips = pygame.sprite.Group(allShips)

    allSprites = pygame.sprite.OrderedUpdates(allShips, highscore_label, instructions_label)

    # ACTION
    # ASSIGN
    keepGoing = True
    clock = pygame.time.Clock()

    # LOOP
    while keepGoing:

        # TIME
        clock.tick(30)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.fadeout(1)
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(1)
                    pygame.quit()
                    return False

        # REFRESH
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()


def game(screen):
    """This is the main function that handles the main logic of the game. It will return the score that was acheived."""
    # DISPLAY
    screen = screen

    # ENTITIES
    background = pygame.image.load("./Sprite/space.png").convert()

    pygame.mixer.music.load("./Sound/laser2.wav")
    pygame.mixer.music.set_volume(0.5)
    gunStop = pygame.mixer.Sound("./Sound/laserstop1.wav")
    gunStop.set_volume(1.0)
    coolMusic = pygame.mixer.Sound("./Sound/music.wav")
    coolMusic.set_volume(0.25)
    coolMusic.play(-1)
    enemyShoot = pygame.mixer.Sound("./Sound/laser1.wav")
    enemyShoot.set_volume(1.0)
    scorekeeper = spaceBattleGameSprites.Scorekeeper(screen)
    lifekeeper = spaceBattleGameSprites.Lifekeeper(screen)
    player = spaceBattleGameSprites.PlayerShip(screen)

    enemyGroup = pygame.sprite.Group(spaceBattleGameSprites.EnemyShip(screen))
    bulletGroup = pygame.sprite.Group()
    powerupGroup = pygame.sprite.Group()

    allSprites = pygame.sprite.OrderedUpdates(bulletGroup, powerupGroup, player, enemyGroup, scorekeeper, lifekeeper)

    # ACTION
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    destroyedShips = 0
    alreadyIncreased = False
    deathCounter = 0

    # LOOP
    while keepGoing:
        # TIME
        clock.tick(30)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_ESCAPE:
                    keepGoing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    gunStop.play()

        # Player ship controls (keyboard)
        if not (player.get_explode() or deathCounter):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.rotate(5)
            if keys[pygame.K_RIGHT]:
                player.rotate(-5)
            if keys[pygame.K_SPACE]:
                bulletGroup.add(spaceBattleGameSprites.Bullet(screen, player, "PLAYER"))
                allSprites = pygame.sprite.OrderedUpdates(bulletGroup, powerupGroup, player, enemyGroup,
                                                          scorekeeper, lifekeeper)
            if keys[pygame.K_a]:
                player.move((-1, 0))
            if keys[pygame.K_d]:
                player.move((1, 0))
            if keys[pygame.K_w]:
                player.move((0, -1))
            if keys[pygame.K_s]:
                player.move((0, 1))

        # if the player is exploding, or is about to be destroyed, then none of the below code will run
        if not (player.get_explode() or deathCounter):
            # If the player is hit by the enemy
            hits = pygame.sprite.spritecollide(player, bulletGroup, False)
            for bullet in hits:
                if bullet.who_shot() == "ENEMY":
                    lifekeeper.take_damage(bullet.get_bullet_damage())
                    bullet.kill()

            # If the Player collides with an enemy they take immense damage and be destroyed!
            for enemy in pygame.sprite.spritecollide(player, enemyGroup, False):
                if not enemy.get_explode():
                    player.explode()
                    deathCounter = 1
                    pygame.mixer.music.stop()

            # Player dies
            if lifekeeper.get_health_points() <= 0:
                player.explode()
                deathCounter = 1
                pygame.mixer.music.stop()

        # if the player collides with a powerup
        hits = pygame.sprite.spritecollide(player, powerupGroup, False)
        for crate in hits:
            if crate.get_type() == 1:
                lifekeeper.increase_health_points(100)
            elif crate.get_type() == 2:
                lifekeeper.increase_shield_points(500)
            elif crate.get_type() == 3:
                player.set_bullet_damage(player.get_bullet_damage() + 1)
            crate.kill()

        # If the enemy is hit by the player
        for enemy in enemyGroup:
            if not enemy.get_explode():
                hits = pygame.sprite.spritecollide(enemy, bulletGroup, False)
                for bullet in hits:
                    if bullet.who_shot() == "PLAYER":
                        enemy.decrease_health_points(bullet.get_bullet_damage())
                        bullet.kill()

        # Enemy ships shoot
        if random.randint(1, 35) == 1:
            for enemy in enemyGroup:
                enemyShoot.play()
                bulletGroup.add(spaceBattleGameSprites.Bullet(screen, enemy, "ENEMY", player))
                allSprites = pygame.sprite.OrderedUpdates(bulletGroup, powerupGroup, player, enemyGroup,
                                                          scorekeeper, lifekeeper)

        # Check the health of the Enemies
        for enemy in enemyGroup:
            if enemy.get_health_points() < 0 and not enemy.get_explode():
                scorekeeper.increase_score(enemy.get_value())
                enemy.explode()
                destroyedShips += 1
                alreadyIncreased = False

        # Increase maximum ships every 10 destroyed
        if destroyedShips % 10 == 0 and not alreadyIncreased:
            enemyGroup.add(pygame.sprite.Group(spaceBattleGameSprites.EnemyShip(screen)))
            allSprites = pygame.sprite.OrderedUpdates(bulletGroup, powerupGroup, player, enemyGroup,
                                                      scorekeeper, lifekeeper)
            alreadyIncreased = True

        # Powerup generation
        if random.randint(1, 500) == 250:
            powerupGroup.add(spaceBattleGameSprites.Powerup(screen, random.randint(1, 3)))
            allSprites = pygame.sprite.OrderedUpdates(bulletGroup, powerupGroup, player, enemyGroup,
                                                      scorekeeper, lifekeeper)

        # Finish player explosion animations before returning
        if deathCounter:
            deathCounter += 1
        if deathCounter == 33:
            keepGoing = False

        # REFRESH
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Return the score
    coolMusic.stop()
    return scorekeeper.get_score()

# Call the main function
main()
