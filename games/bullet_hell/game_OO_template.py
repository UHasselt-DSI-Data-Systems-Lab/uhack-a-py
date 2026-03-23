#################################################################
# OOP code                                                      #
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


#################################################################
# Variabelen en klassen                                         #
#################################################################


# Definieer globale constanten voor schermgrootte
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# Define classes
class Player:
    def __init__(self, x, y, size, speed):
        self.position = Vector(x, y)
        self.size = size
        self.speed = speed
        self.direction = Vector(0, 0)

    def handle_input(self):
        # Reset de richting elke frame, beweeg de speler met de pijltjestoetsen en update self.direction
        # (Vergeet niet de speler binnen het scherm te houden!)
        # TODO: Opdracht 3
        pass

    def move(self):
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed

    def draw(self):
        # Teken de speler met de "mage.png" afbeelding op self.position met self.size als breedte en hoogte
        # TODO: Opdracht 2
        pass

    def get_rect(self):
        return rectangle(self.position.x, self.position.y, self.size, self.size, colors.SKYBLUE)


class Enemy:
    def __init__(self, x, y, size, speed):
        self.position = Vector(x, y)
        self.size = size
        self.speed = speed

    def move(self, player_x, player_y):
        # Beweeg de vijand stap voor stap naar de speler toe (vergelijk x en y apart)
        # TODO: Opdracht 5
        pass

    def draw(self):
        # Teken de vijand met de "enemy.png" afbeelding op self.position met self.size als breedte en hoogte
        # TODO: Opdracht 4
        pass

    def get_rect(self):
        return rectangle(self.position.x, self.position.y, self.size, self.size, colors.INDIANRED)


class Bullet:
    def __init__(self, x, y, size, speed, direction):
        self.position = Vector(x, y)
        self.size = size
        self.speed = speed
        self.direction = direction

    def move(self):
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed

    def draw(self):
        # Teken de kogel met de "bullet.png" afbeelding op self.position met self.size als breedte en hoogte
        # TODO: Opdracht 6
        pass

    def is_out_of_screen(self):
        return out_of_screen(self.position.x, self.position.y)

    def get_rect(self):
        return rectangle(self.position.x, self.position.y, self.size, self.size, colors.YELLOW)


#################################################################
# Game logica : gegeven code                                    #
#################################################################


class Game:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 150, 5.5)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.highscore = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.bullet_cooldown = 0
        self.enemy_speed = 2
        self.enemy_size = 150
        self.bullet_speed = 15
        self.bullet_size = 50

    def reset(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 150, 5.5)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.bullet_cooldown = 0

    def run(self):
        while playing():
            if self.game_over:
                self.show_game_over()
                continue

            #################################################################
            # Spel logica : aan te passen code                              #
            #################################################################

            self.handle_input()
            self.update_game_state()

            #################################################################
            # Tekenfase                                                     #
            #################################################################

            self.draw_elements()

    def handle_input(self):
        # Laat de speler bewegen
        self.player.handle_input()

        # Schiet een kogel in de richting van de speler als de cooldown 0 is en de speler beweegt
        # (Hint: gebruik self.player.direction en maak een nieuwe Bullet aan met Bullet(x, y, size, speed, richting))
        # TODO: Opdracht 7
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def draw_elements(self):
        # Teken de achtergrond, vijanden, kogels, speler en scores
        # TODO: Opdracht 1: Teken hier een lichtgroene cirkel als speler (mag verwijderd worden na opdracht 2)

        # Teken de achtergrond, vijanden, kogels, speler en scores
        # TODO: Opdracht 8
        pass

    #################################################################
    # Gegeven code                                                  #
    #################################################################

    def update_game_state(self):
        # Speler en objecten bewegen
        self.player.move()
        for enemy in self.enemies:
            enemy.move(self.player.position.x, self.player.position.y)
        for bullet in self.bullets:
            bullet.move()

        # Vijanden spawnen en kogels buiten het scherm verwijderen
        self.spawn_enemies()
        self.remove_bullets_out_of_screen()

        # Botsingen detecteren
        self.detect_collisions()

    def detect_collisions(self):
        # Botsingen tussen kogels en vijanden detecteren
        new_enemies = []
        for enemy in self.enemies:
            hit = False
            for bullet in self.bullets:
                if collide(enemy.get_rect(), bullet.get_rect()):
                    self.score += 1
                    hit = True
                    self.bullets.remove(bullet)
                    break
            if not hit:
                new_enemies.append(enemy)
        self.enemies = new_enemies

        # Botsingen tussen speler en vijanden detecteren
        player_rect = self.player.get_rect()
        for enemy in self.enemies:
            if collide(player_rect, enemy.get_rect()):
                if self.score > self.highscore:
                    self.highscore = self.score
                self.game_over = True
                break

    def show_game_over(self):
        image("bg.png", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 180))
        text(SCREEN_WIDTH // 2, 400, "Game Over!", colors.YELLOW, size=100, align="center")
        text(SCREEN_WIDTH // 2, 500, f"Score: {self.score}", colors.WHITE, size=100, align="center")
        text(SCREEN_WIDTH // 2, 600, f"Highscore: {self.highscore}", colors.SKYBLUE, size=80, align="center")
        text(SCREEN_WIDTH // 2, 700, "Press R to Restart", colors.YELLOW, size=40, align="center")
        if input(K_r):
            self.reset()

    def remove_bullets_out_of_screen(self):
        self.bullets = [b for b in self.bullets if not b.is_out_of_screen()]

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer > 60:
            spawn_edge = random.choice(['top', 'bottom', 'left', 'right'])
            if spawn_edge == 'top':
                x, y = random.randint(0, SCREEN_WIDTH), 0
            elif spawn_edge == 'bottom':
                x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
            elif spawn_edge == 'left':
                x, y = 0, random.randint(0, SCREEN_HEIGHT)
            else:
                x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
            self.enemies.append(Enemy(x, y, self.enemy_size, self.enemy_speed))
            self.enemy_spawn_timer = 0


# Maak het spel aan en start het
game = Game()
game.run()