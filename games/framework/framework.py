#################################################################
# Use the packages from the portable Python environment         #
#################################################################

import os, sys

# Locate the libs folder of the portable Python environment
def find_python_libs():
    start_path = os.path.abspath(os.path.dirname(__file__))
    current = start_path
    while True:
        parent = os.path.dirname(current)
        if parent == current:  # reached filesystem root
            break
        candidate = os.path.join(parent, 'SystemEnv', 'Python', 'python', 'libs')
        if os.path.isdir(candidate):
            return os.path.abspath(candidate)
        current = parent
    return None

_python_libs = find_python_libs()
if _python_libs and _python_libs not in sys.path:
    sys.path.insert(0, _python_libs)



#################################################################
# Framework code                                               #
#################################################################

# Imports
import pygame
from pygame.locals import QUIT
import games.framework.backend as backend

# Run the backend
backend.start()



### Main function ###

# Main game loop function, returns False if the game should end
def playing():
    backend.present_frame()
    pygame.display.flip()
    backend.CLOCK.tick(60)  # limits FPS to 60

    backend.previous_keys = backend.current_keys

    # Handle the quit event
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            backend.playing = False
            return False

    backend.current_keys = pygame.key.get_pressed()

    backend.GAME_SURFACE.fill(backend.BACKGROUND)

    return backend.playing



### Input functions ###

# Returns True if the specified key is currently held down
def input(key):
    keys = pygame.key.get_pressed()
    return keys[key]

# Returns True if the specified key was pressed down this frame (not held)
def input_once(key):
    return backend.current_keys[key] and not backend.previous_keys[key]



### Drawing functions ###

def rectangle(x, y, w, h, color):
    y = backend.HEIGHT - y - h  # Invert y-axis to match traditional coordinate system
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(backend.GAME_SURFACE, color, rect)
    return rect

def circle(x, y, w, h, color):
    y = backend.HEIGHT - y - h  # Invert y-axis to match traditional coordinate system
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.ellipse(backend.GAME_SURFACE, color, rect)
    return rect


HORIZONTAL_FLIP = (pygame.transform.flip, (True, False))
VERTICAL_FLIP = (pygame.transform.flip, (False, True))

# Draw an image on the screen with optional transformations
# Transforms is a list of tuples: (function, args), eg. [(HORIZONTAL_FLIP), (pygame.transform.scale, (100, 50))]
def image(image_name, x, y, w, h, transforms=[]):
    y = backend.HEIGHT - y - h  # Invert y-axis to match traditional coordinate system
    # Check if the image is already loaded
    for img_data in backend.loaded_images:
        if img_data[0] != image_name:
            continue
        if img_data[2] != w or img_data[3] != h:
            continue
        if img_data[4] != transforms:
            continue
        backend.GAME_SURFACE.blit(img_data[1], (x, y))
        return img_data[1]

    # Load and scale the image, then store it in the loaded_images list
    img = pygame.image.load(f"./images/{image_name}").convert_alpha()
    img = pygame.transform.scale(img, (w, h))
    if transforms:
        for transform_func, args in transforms:
            img = transform_func(img, *args)
    backend.loaded_images.append((image_name, img, w, h, transforms))
    backend.GAME_SURFACE.blit(img, (x, y))
    return img


# Draw text on the screen with alignment options
# Align options:
#  - topleft (default), midtop, topright,
#  - midleft, center, midright,
#  - bottomleft, midbottom, bottomright
def text(x, y, content, color, size=30, align="topleft"):
    if align == "center":
        x -= size * len(content) // 4  # Roughly center the text based on its length
    elif align == "topright":
        x -= size * len(content) // 2
    elif align == "midtop":
        x -= size * len(content) // 4
        y -= size // 2
    elif align == "midbottom":
        x -= size * len(content) // 4
        y += size // 2
    elif align == "bottomright":
        x -= size * len(content) // 2
        y += size
    elif align == "bottomleft":
        y += size
    elif align == "midleft":
        y -= size // 2
    elif align == "midright":
        x -= size * len(content) // 2
        y -= size // 2

    y = backend.HEIGHT - y  # Invert y-axis to match traditional coordinate system
    font = pygame.font.Font(None, size)
    text_surface = font.render(content, True, color)
    backend.GAME_SURFACE.blit(text_surface, (x, y - size))  # Adjust y to account for text height
    return text_surface.get_rect(topleft=(x, y - size))


# Check for collision between two objects (must both be rectangles or both be images)
def collide(obj1, obj2):
    # If obj1 and obj2 are rectangles
    if isinstance(obj1, pygame.Rect) and isinstance(obj2, pygame.Rect):
        return obj1.colliderect(obj2)

    # If obj1 and obj2 are images (surfaces)
    elif isinstance(obj1, pygame.Surface) and isinstance(obj2, pygame.Surface):
        mask1 = pygame.mask.from_surface(obj1)
        mask2 = pygame.mask.from_surface(obj2)
        offset = (obj2.get_rect().x - obj1.get_rect().x, obj2.get_rect().y - obj1.get_rect().y)
        return mask1.overlap(mask2, offset) is not None

    return TypeError("Both objects must be either pygame.Rect or pygame.Surface instances.")


# Check if a point is out of the screen bounds
def out_of_screen(x, y):
    return x < 0 or x > backend.WIDTH or y < 0 or y > backend.HEIGHT