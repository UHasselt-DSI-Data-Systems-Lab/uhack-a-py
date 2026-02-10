import pygame

BACKGROUND = (255, 255, 255)
LETTERBOX_COLOR = (0, 0, 0)
WINDOW = None
GAME_SURFACE = None
CLOCK = None
HEIGHT = 1080  # Logical height the games are built against
WIDTH = 1920   # Logical width the games are built against
DISPLAY_WIDTH = None
DISPLAY_HEIGHT = None
SCALE = 1
SCALED_WIDTH = WIDTH
SCALED_HEIGHT = HEIGHT
OFFSET_X = 0
OFFSET_Y = 0

playing = False
loaded_images = [] # [(image_name, image_surface, width, height, transforms)]

current_keys = None
previous_keys = None


def start():
    global WINDOW, GAME_SURFACE, playing, CLOCK, current_keys, previous_keys
    global DISPLAY_WIDTH, DISPLAY_HEIGHT

    pygame.init()
    CLOCK = pygame.time.Clock()

    display_info = pygame.display.Info()
    DISPLAY_WIDTH = display_info.current_w
    DISPLAY_HEIGHT = display_info.current_h

    WINDOW = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
    pygame.display.set_caption('My Game!')

    GAME_SURFACE = pygame.Surface((WIDTH, HEIGHT)).convert()
    GAME_SURFACE.fill(BACKGROUND)

    _recalculate_scale()

    present_frame()
    pygame.display.flip()

    previous_keys = pygame.key.get_pressed()
    current_keys = pygame.key.get_pressed()

    playing = True


def _recalculate_scale():
    global SCALE, SCALED_WIDTH, SCALED_HEIGHT, OFFSET_X, OFFSET_Y

    width_ratio = DISPLAY_WIDTH / WIDTH
    height_ratio = DISPLAY_HEIGHT / HEIGHT
    SCALE = min(width_ratio, height_ratio)

    SCALED_WIDTH = int(WIDTH * SCALE)
    SCALED_HEIGHT = int(HEIGHT * SCALE)
    OFFSET_X = (DISPLAY_WIDTH - SCALED_WIDTH) // 2
    OFFSET_Y = (DISPLAY_HEIGHT - SCALED_HEIGHT) // 2


def present_frame():
    if WINDOW is None or GAME_SURFACE is None:
        return

    WINDOW.fill(LETTERBOX_COLOR)

    if SCALE != 1:
        scaled_surface = pygame.transform.smoothscale(GAME_SURFACE, (SCALED_WIDTH, SCALED_HEIGHT))
    else:
        scaled_surface = GAME_SURFACE

    WINDOW.blit(scaled_surface, (OFFSET_X, OFFSET_Y))