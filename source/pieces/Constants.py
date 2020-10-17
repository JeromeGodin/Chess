from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1


class Type(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


class Direction(Enum):
    UP = (-1, 0)
    UP_RIGHT = (-1, 1)
    RIGHT = (0, 1)
    DOWN_RIGHT = (1, 1)
    DOWN = (1, 0)
    DOWN_LEFT = (1, -1)
    LEFT = (0, -1)
    UP_LEFT = (-1, -1)
    L_UP_RIGHT = (-2, 1)
    L_RIGHT_UP = (-1, 2)
    L_RIGHT_DOWN = (1, 2)
    L_DOWN_RIGHT = (2, 1)
    L_DOWN_LEFT = (2, -1)
    L_LEFT_DOWN = (1, -2)
    L_LEFT_UP = (-1, -2)
    L_UP_LEFT = (-2, -1)


class Capture(Enum):
    NO = 0
    YES = 1
    MANDATORY = 2
