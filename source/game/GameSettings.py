import math
from enum import Enum


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
YELLOW = (186, 202, 68, 255)

POSSIBLE_MOVE_RADIUS = int(math.floor(TILE_SIZE_IN_PIXELS * 0.2))
POSSIBLE_CAPTURE_RADIUS = int(math.floor(POSSIBLE_MOVE_RADIUS) * 2.5)
POSSIBLE_MOVE_COLOR = (150, 150, 150, 10)
POSSIBLE_CAPTURE_WIDTH = int(math.floor(TILE_SIZE_IN_PIXELS * 0.08))
HOVERED_TILE_BORDER_WIDTH = 5

PROMOTION_WINDOW_COLOR = (255, 255, 255, 255)
PROMOTION_WINDOW_HOVER_COLOR = (200, 200, 200, 255)


class GameStatus(Enum):
    MENU = 0
    IN_PROGRESS = 1
    OVER = 2


class GameResult(Enum):
    VICTORY = 0
    DEFEAT = 1
    DRAW = 2


class GameFinish(Enum):
    CHECKMATE = 0
    STALEMATE = 1
    REPETITION = 2
    INSUFFICIENT_MATERIAL = 3
    FIFTY_MOVES = 4
    TIMEOUT = 5
