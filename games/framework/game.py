from framework import *
from pygame.locals import *
import colors

x = 0
y = 0
speed = 10

while playing():
    if input(K_RIGHT):
        x += speed
    if input(K_LEFT):
        x -= speed
    if input(K_UP):
        y -= speed
    if input(K_DOWN):
        y += speed

    rectangle(x, y, 100, 100, colors.INDIANRED)
    image("template.png", x + 100, y + 100, 200, 200)