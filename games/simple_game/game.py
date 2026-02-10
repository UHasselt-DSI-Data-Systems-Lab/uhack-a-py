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
    global coins, score

    # Botsingen tussen munten en de speler detecteren
    for coin in coins[:]:
        coin_rect = rectangle(coin[X], coin[Y], coin_size, coin_size, colors.GOLD)
        player_rect = rectangle(player_position[X], player_position[Y], player_size, player_size, colors.SKYBLUE)
        if collide(player_rect, coin_rect):
            coins.remove(coin)
            score += 1

def spawn_coin():
    global coins
    x = random.randint(0, SCREEN_WIDTH - coin_size)
    y = random.randint(0, SCREEN_HEIGHT - coin_size)
    coins.append([x, y])

def show_game_over():
    global score, highscore, player_position, coins, timer
    if score > highscore:
        highscore = score
    rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 180))
    text(SCREEN_WIDTH // 2, 400, "Game Over!", colors.YELLOW, size=100, align="center")
    text(SCREEN_WIDTH // 2, 500, f"Score: {score}", colors.WHITE, size=100, align="center")
    text(SCREEN_WIDTH // 2, 600, f"Highscore: {highscore}", colors.SKYBLUE, size=80, align="center")
    text(SCREEN_WIDTH // 2, 700, "Press R to Restart", colors.YELLOW, size=40, align="center")
    if input(K_r):
        player_position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        coins = []
        score = 0
        timer = 60

#################################################################
# Variabelen                                                    #
#################################################################

X = 0
Y = 1
X_DIRECTION = 2
Y_DIRECTION = 3
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

score = 0
highscore = 0
gameOver = False

player_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_size = 100
player_speed = 10
player_direction = [0, 0]

coins = []
coin_size = 50

timer = 60

#################################################################
# Spel logica                                                   #
#################################################################

while playing():
    if timer <= 0:
        show_game_over()
    else: 
        rectangle(player_position[X], player_position[Y], player_size, player_size, colors.SKYBLUE)

        # Input verwerken
        if input(K_LEFT):
            player_position[X] -= player_speed
        if input(K_RIGHT):
            player_position[X] += player_speed
        if input(K_UP):
            player_position[Y] += player_speed
        if input(K_DOWN):
            player_position[Y] -= player_speed

        # Binnen de schermgrenzen blijven
        if player_position[X] < 0:
            player_position[X] = 0
        if player_position[X] > SCREEN_WIDTH - player_size:
            player_position[X] = SCREEN_WIDTH - player_size
        if player_position[Y] < 0:
            player_position[Y] = 0
        if player_position[Y] > SCREEN_HEIGHT - player_size:
            player_position[Y] = SCREEN_HEIGHT - player_size
        
        # Munten tekenen en botsingen detecteren
        detect_collisions()
        if coins == []:
            spawn_coin()

        # Score en timer weergeven
        text(20, 20, f"Score: {score}", colors.BLACK)
        text(20, 60, f"Time: {int(timer)}", colors.BLACK)

        # Aftellen van de timer
        timer -= 1 / 60