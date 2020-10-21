from enum import Enum


GAME_RESULT_WINDOW_POSITION = (250, 150)
GAME_RESULT_WINDOW_SIZE = (300, 400)


class GameResultResponse(Enum):
    REMATCH = 0
    REVIEW = 1
    MENU = 2
