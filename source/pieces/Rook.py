import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class Rook(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.ROOK, 'R', 5)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wr100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\br100'
                                                                                       '.png')
        # self.image = pg.transform.scale(self.image, (settings.TILE_SIZE_IN_PIXELS, settings.TILE_SIZE_IN_PIXELS))
        self._available_moves = [
            Move(constants.Direction.UP, 7, constants.Capture.YES, False),
            Move(constants.Direction.RIGHT, 7, constants.Capture.YES, False),
            Move(constants.Direction.DOWN, 7, constants.Capture.YES, False),
            Move(constants.Direction.LEFT, 7, constants.Capture.YES, False)]
