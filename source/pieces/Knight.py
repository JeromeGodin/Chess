import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class Knight(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.KNIGHT, 'N', 3)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wn100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\bn100'
                                                                                       '.png')
        # self.image = pg.transform.scale(self.image, (settings.TILE_SIZE_IN_PIXELS, settings.TILE_SIZE_IN_PIXELS))
        self._available_moves = [
            Move(constants.Direction.L_UP_RIGHT, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_RIGHT_UP, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_RIGHT_DOWN, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_DOWN_RIGHT, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_DOWN_LEFT, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_LEFT_DOWN, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_LEFT_UP, 1, constants.Capture.YES, False),
            Move(constants.Direction.L_UP_LEFT, 1, constants.Capture.YES, False)]
