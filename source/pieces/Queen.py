import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class Queen(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.QUEEN, 9)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wq100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\bq100'
                                                                                       '.png')
        # self.image = pg.transform.scale(self.image, (settings.TILE_SIZE_IN_PIXELS, settings.TILE_SIZE_IN_PIXELS))
        self._available_moves = [
            Move(constants.Direction.UP, 7, constants.Capture.YES, False),
            Move(constants.Direction.UP_RIGHT, 7, constants.Capture.YES, False),
            Move(constants.Direction.RIGHT, 7, constants.Capture.YES, False),
            Move(constants.Direction.DOWN_RIGHT, 7, constants.Capture.YES, False),
            Move(constants.Direction.DOWN, 7, constants.Capture.YES, False),
            Move(constants.Direction.DOWN_LEFT, 7, constants.Capture.YES, False),
            Move(constants.Direction.LEFT, 7, constants.Capture.YES, False),
            Move(constants.Direction.UP_LEFT, 7, constants.Capture.YES, False)]
