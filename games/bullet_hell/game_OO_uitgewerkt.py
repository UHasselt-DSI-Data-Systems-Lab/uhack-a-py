#################################################################
# Ingevulde OOP code                                            #
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
        # Reset de richting elke frame
        self.direction = Vector(0, 0)
        # Beweeg de speler met de pijltjestoetsen en update de richting
        if input(K_LEFT):
            self.direction.x = -1
        if input(K_RIGHT):
            self.direction.x = 1
        if input(K_UP):
            self.direction.y = 1
        if input(K_DOWN):
            self.direction.y = -1
        # Houd de speler binnen het scherm
        self.position.x = max(0, min(SCREEN_WIDTH - self.size, self.position.x))
        self.position.y = max(0, min(SCREEN_HEIGHT - self.size, self.position.y))

    def move(self):
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed

    def draw(self):
        # Teken de speler op zijn positie
        image("mage.png", self.position.x, self.position.y, self.size, self.size)

    def get_rect(self):
        return rectangle(self.position.x, self.position.y, self.size, self.size, colors.SKYBLUE)


class Enemy:
    def __init__(self, x, y, size, speed):
        self.position = Vector(x, y)
        self.size = size
        self.speed = speed

    def move(self, player_x, player_y):
        # Beweeg de vijand stap voor stap naar de speler
        if self.position.x < player_x:
            self.position.x += self.speed
        if self.position.x > player_x:
            self.position.x -= self.speed
        if self.position.y < player_y:
            self.position.y += self.speed
        if self.position.y > player_y:
            self.position.y -= self.speed

    def draw(self):
        # Teken de vijand op zijn positie
        image("enemy.png", self.position.x, self.position.y, self.size, self.size)

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
        # Teken de kogel op zijn positie
        image("bullet.png", self.position.x, self.position.y, self.size, self.size)

    def is_out_of_screen(self):
        return out_of_screen(self.position.x, self.position.y)

    def get_rect(self):
        return rectangle(self.position.x, self.position.y, self.size, self.size, colors.YELLOW)


#################################################################
# Game logica                                                   #
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

            self.handle_input()
            self.update_game_state()

            self.draw_elements()

    def handle_input(self):
        # Laat de speler bewegen
        self.player.handle_input()

        # Schiet een kogel als de cooldown 0 is en de speler beweegt
        if self.bullet_cooldown <= 0:
            if self.player.direction != Vector(0, 0):
                bullet_x = self.player.position.x + 25
                bullet_y = self.player.position.y + 25
                bullet_dir = self.player.direction.normalize()
                self.bullets.append(Bullet(bullet_x, bullet_y, self.bullet_size, self.bullet_speed, bullet_dir))
                self.bullet_cooldown = 30
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def draw_elements(self):
        # Teken de achtergrond
        image("bg.png", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Teken vijanden, kogels en speler
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        self.player.draw()

        # Teken de scores
        text(20, 20, f"Score: {self.score}", colors.WHITE)
        text(20, 60, f"Highscore: {self.highscore}", colors.SKYBLUE)

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