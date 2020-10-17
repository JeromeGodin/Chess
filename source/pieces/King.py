import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class King(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.KING, 0)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wk100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\bk100'
                                                                                       '.png')
        self._available_moves = [
            Move(constants.Direction.UP, 1, constants.Capture.YES, False),
            Move(constants.Direction.UP_RIGHT, 1, constants.Capture.YES, False),
            Move(constants.Direction.RIGHT, 1, constants.Capture.YES, False),
            Move(constants.Direction.DOWN_RIGHT, 1, constants.Capture.YES, False),
            Move(constants.Direction.DOWN, 1, constants.Capture.YES, False),
            Move(constants.Direction.DOWN_LEFT, 1, constants.Capture.YES, False),
            Move(constants.Direction.LEFT, 1, constants.Capture.YES, False),
            Move(constants.Direction.UP_LEFT, 1, constants.Capture.YES, False),
            Move(constants.Direction.RIGHT, 2, constants.Capture.YES, True),
            Move(constants.Direction.LEFT, 2, constants.Capture.YES, True)]
