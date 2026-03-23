#################################################################
# Gegeven code                                                  #
#################################################################

# Python
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Framework imports en pygame essentials
from games.framework.framework import *
import games.framework.colors as colors
from pygame.locals import *

# Extra imports
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


# Constanten voor betere leesbaarheid
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Info over de speler
player_position = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
player_speed = 5.5
player_direction = Vector(0, 0)
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
        # TODO: Opdracht 3: Vul hier de code in om de speler te laten bewegen met pijltjestoetsen

        # Vijanden naar de speler laten bewegen
        # TODO: Opdracht 5: Vul hier de code in om vijanden naar de speler te laten bewegen

        # Vijanden spawnen aan de randen van het scherm
        spawn_enemies()

        # Kogels buiten het scherm verwijderen
        remove_bullets_out_of_screen()

        # Kogels schieten wanneer je ergens naar beweegt
        # TODO: Opdracht 6, 7, 9: Vul hier de code in om kogels te schieten wanneer de speler beweegt

        # Kogels laten bewegen
        # TODO: Opdracht 8: Vul hier de code in om kogels te laten bewegen

        # Botsingen detecteren tussen kogels, vijanden en de speler
        detect_collisions()


        #################################################################
        # Tekenfase                                                     #
        #################################################################


        # Achtergrond tekenen
        bg = image("bg.png", 0, 0, 1920, 1080)

        # Speler, enemies en kogels tekenen
        # TODO: Opdracht 1: Hier mag de cirkel getekend worden. Deze mag verwijderd worden voor je begint aan opdracht 2.

        # TODO: Opdracht 2, 4, 8: Vul hier de code in om de speler, enemies en kogels te tekenen

        # Scores tekenen
        text(20, 20, f"Score: {score}", colors.WHITE)
        text(20, 60, f"Highscore: {highscore}", colors.SKYBLUE)