import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class Pawn(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.PAWN, 1)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wp100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\bp100'
                                                                                       '.png')
        # self.image = pg.transform.scale(self.image, (settings.TILE_SIZE_IN_PIXELS, settings.TILE_SIZE_IN_PIXELS))
        self._available_moves = [
            Move(constants.Direction.UP, 1, constants.Capture.NO, False),
            Move(constants.Direction.UP, 2, constants.Capture.NO, True),
            Move(constants.Direction.UP_LEFT, 1, constants.Capture.MANDATORY, False),
            Move(constants.Direction.UP_RIGHT, 1, constants.Capture.MANDATORY, False)]
