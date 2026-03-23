#################################################################
# Gegeven code                                                  #
#################################################################

# python
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# now the existing import will find the top-level `games` package

from games.framework.framework import *
import games.framework.colors as colors
from pygame.locals import *
import random


def detect_collisions():
    global score, highscore, game_over, enemies

    # Botsingen tussen kogels en enemies detecteren
    new_enemies = []
    for enemy in enemies:
        enemy_rect = rectangle(enemy.x, enemy.y, enemy_size, enemy_size, colors.INDIANRED)
        hit = False
        for bullet_position in bullet_positions:
            proj_rect = rectangle(bullet_position.x, bullet_position.y, bullet_size, bullet_size, colors.YELLOW)
            if collide(enemy_rect, proj_rect):
                score += 1
                hit = True
                break
        if not hit:
            new_enemies.append(enemy)
    enemies = new_enemies

    # Botsingen tussen speler en enemies detecteren
    player_rect = rectangle(player_position.x, player_position.y, player_size, player_size, colors.SKYBLUE)
    for enemy in enemies:
        enemy_rect = rectangle(enemy.x, enemy.y, enemy_size, enemy_size, colors.INDIANRED)
        if collide(player_rect, enemy_rect):
            if score > highscore:
                highscore = score
            game_over = True
            break


def show_game_over():
    global player_position, enemies, bullet_positions, bullet_directions, score, player_direction, enemy_spawn_timer, bullet_cooldown, game_over

    image("bg.png", 0, 0, 1920, 1080)
    rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 180))
    text(SCREEN_WIDTH // 2, 400, "Game Over!", colors.YELLOW, size=100, align="center")
    text(SCREEN_WIDTH // 2, 500, f"Score: {score}", colors.WHITE, size=100, align="center")
    text(SCREEN_WIDTH // 2, 600, f"Highscore: {highscore}", colors.SKYBLUE, size=80, align="center")
    text(SCREEN_WIDTH // 2, 700, "Press R to Restart", colors.YELLOW, size=40, align="center")
    if input(K_r):
        player_position = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        enemies = []
        bullet_positions = []
        bullet_directions = []
        score = 0
        player_direction = Vector(0, 0)
        enemy_spawn_timer = 0
        bullet_cooldown = 0
        game_over = False


def remove_bullets_out_of_screen():
    global bullet_positions, bullet_directions
    bullet_directions = [bullet_direction for (bullet_position, bullet_direction) in zip(bullet_positions, bullet_directions) if not out_of_screen(bullet_position.x, bullet_position.y)] 
    bullet_positions = [bullet_position for bullet_position in bullet_positions if not out_of_screen(bullet_position.x, bullet_position.y)]


def spawn_enemies():
    global enemy_spawn_timer, enemies

    enemy_spawn_timer += 1
    if enemy_spawn_timer > 60:
        spawn_edge = random.choice(['top', 'bottom', 'left', 'right'])
        if spawn_edge == 'top':
            enemies.append(Vector(random.randint(0, 1920), 0))
        elif spawn_edge == 'bottom':
            enemies.append(Vector(random.randint(0, 1920), 1080))
        elif spawn_edge == 'left':
            enemies.append(Vector(0, random.randint(0, 1080)))
        else:
            enemies.append(Vector(1920, random.randint(0, 1080)))
        enemy_spawn_timer = 0


#################################################################
# Variabelen                                                    #
#################################################################


# Constantes voor betere leesbaarheid
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Info over de speler
player_position = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
player_direction = Vector(0, 0)
player_speed = 5.5
player_size = 150

# Info over de vijanden
enemies = []
enemy_spawn_timer = 0
enemy_speed = 2
enemy_size = 150

# Info over de kogels
bullet_positions = []
bullet_directions = []
bullet_speed = 15
bullet_cooldown = 0
bullet_size = 50

# Scores
score = 0
highscore = 0
game_over = False

#################################################################
# Spel logica                                                   #
#################################################################

while playing():
    # Het game over scherm tonen als het spel afgelopen is
    if game_over:
        show_game_over()

    # Anders het spel laten lopen
    else:
        # De speler laten bewegen met pijltjestoetsen
        player_direction = Vector(0, 0)
        if input(K_LEFT):
            player_position.x -= player_speed
            player_direction.x = -1
        if input(K_RIGHT):
            player_position.x += player_speed
            player_direction.x = 1
        if input(K_UP):
            player_position.y += player_speed
            player_direction.y = 1
        if input(K_DOWN):
            player_position.y -= player_speed
            player_direction.y = -1


        # Vijanden naar de speler laten bewegen
        for enemy in enemies:
            if enemy.x < player_position.x:
                enemy.x += enemy_speed
            if enemy.x > player_position.x:
                enemy.x -= enemy_speed
            if enemy.y < player_position.y:
                enemy.y += enemy_speed
            if enemy.y > player_position.y:
                enemy.y -= enemy_speed

        # Vijanden spawnen aan de randen van het scherm
        spawn_enemies()

        # Kogels buiten het scherm verwijderen
        remove_bullets_out_of_screen()

        # Kogels schieten wanneer je ergens naar beweegt
        if bullet_cooldown > 0:
            bullet_cooldown -= 1
        else:
            if player_direction != Vector(0, 0):
                new_bullet_position = Vector(player_position.x + 25, player_position.y + 25)

                new_bullet_direction = player_direction.normalize()

                # Dit is zeker ook oke!
                # new_bullet_direction = Vector(0, 0)
                # if player_direction.x > 0:
                #     if player_direction.y > 0:
                #         new_bullet_direction = Vector(1, 1)
                #     elif player_direction.y < 0:
                #         new_bullet_direction = Vector(1, -1)
                #     else:
                #         new_bullet_direction = Vector(1, 0)
                # elif player_direction.x < 0:
                #     if player_direction.y > 0:
                #         new_bullet_direction = Vector(-1, 1)
                #     elif player_direction.y < 0:
                #         new_bullet_direction = Vector(-1, -1)
                #     else:
                #         new_bullet_direction = Vector(-1, 0)
                # else:
                #     if player_direction.y > 0:
                #         new_bullet_direction = Vector(0, 1)
                #     elif player_direction.y < 0:
                #         new_bullet_direction = Vector(0, -1)

                bullet_positions.append(new_bullet_position)
                bullet_directions.append(new_bullet_direction)
                bullet_cooldown = 30  # Cooldown tijd voordat de volgende kogel kan worden geschoten

        # Kogels laten bewegen
        for (position, direction) in zip(bullet_positions, bullet_directions):
            position.x += direction.x * bullet_speed
            position.y += direction.y * bullet_speed

        # Example for cursor support:
        # if input_mouse(0):
        #     mouse_pos = mouse_position()
        #     for enemy in enemies:
        #         enemy_rect = rectangle(enemy.x, enemy.y, enemy_size, enemy_size, colors.INDIANRED)
        #         if collide(enemy_rect, mouse_pos):
        #             score += 1
        #             enemies.remove(enemy)
        #             break

        # Botsingen detecteren tussen kogels, vijanden en de speler
        detect_collisions()


        #################################################################
        # Tekenfase                                                     #
        #################################################################

        # Achtergrond tekenen
        bg = image("bg.png", 0, 0, 1920, 1080)

        # Speler, enemies en kogels tekenen
        for enemy in enemies:
            image("enemy.png", enemy.x, enemy.y, enemy_size, enemy_size)
        for position in bullet_positions:
            image("bullet.png", position.x, position.y, bullet_size, bullet_size)
        speler = image("mage.png", player_position.x, player_position.y, player_size, player_size)

        # Scores tekenen
        text(20, 20, f"Score: {score}", colors.WHITE)
        text(20, 60, f"Highscore: {highscore}", colors.SKYBLUE)