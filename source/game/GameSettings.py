import math


PLAYER_COUNT = 2

TILE_SIZE_IN_PIXELS = 100
RANK_COUNT = 8
FILE_COUNT = 8
BOARD_SIZE = (RANK_COUNT, FILE_COUNT)

DISPLAY_WIDTH = FILE_COUNT * TILE_SIZE_IN_PIXELS
DISPLAY_HEIGHT = RANK_COUNT * TILE_SIZE_IN_PIXELS

GREEN = (118, 150, 86, 255)
BEIGE = (238, 238, 210, 255)
RED = (160, 0, 0, 255)

POSSIBLE_MOVE_RADIUS = int(math.floor(TILE_SIZE_IN_PIXELS * 0.2))
POSSIBLE_MOVE_COLOR = (100, 100, 100, 10)
