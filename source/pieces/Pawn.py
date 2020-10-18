import pygame as pg
from source.pieces.Piece import Piece
from source.pieces import Constants as constants
from source.pieces.Move import Move


class Pawn(Piece):
    def __init__(self, owner, board_position, display_position, color):
        super().__init__(owner, board_position, display_position, color, constants.Type.PAWN, '', 1)
        self.image = pg.image.load(
            'assets\\images\\pieces\\wp100.png' if color == constants.Color.WHITE else 'assets\\images\\pieces\\bp100'
                                                                                       '.png')
        # self.image = pg.transform.scale(self.image, (settings.TILE_SIZE_IN_PIXELS, settings.TILE_SIZE_IN_PIXELS))
        self.could_get_captured_en_passant = False
        self.ready_for_promotion = False
        self._available_moves = [
            Move(constants.Direction.UP, 1, constants.Capture.NO, False),
            Move(constants.Direction.UP, 2, constants.Capture.NO, True),
            Move(constants.Direction.UP_RIGHT, 1, constants.Capture.MANDATORY, False),
            Move(constants.Direction.UP_LEFT, 1, constants.Capture.MANDATORY, False),
            Move(constants.Direction.UP_RIGHT, 1, constants.Capture.MANDATORY, False,
                 self._get_en_passant_possible_move),
            Move(constants.Direction.UP_LEFT, 1, constants.Capture.MANDATORY, False,
                 self._get_en_passant_possible_move)]

    def _get_en_passant_possible_move(self, move, pieces, board):
        play_direction = 1 - 2 * self.owner
        possible_move = None

        pawn = self.get_en_passant_pawn(move.direction.value[1] * play_direction, pieces)

        if pawn is not None:
            target_position = (self.board_position[0] + move.direction.value[0] * play_direction,
                               self.board_position[1] + move.direction.value[1] * play_direction)
            possible_move = self._get_possible_move(target_position,
                                                    board.tiles[target_position[0]][target_position[1]],
                                                    True)

        return possible_move

    def get_en_passant_pawn(self, move_horizontal_direction, pieces):
        pawn = None

        for piece in pieces:
            if piece.piece == constants.Type.PAWN and piece.owner != self.owner:
                if piece.could_get_captured_en_passant and piece.board_position[0] == self.board_position[0] and \
                        piece.board_position[1] == self.board_position[1] + move_horizontal_direction:
                    pawn = piece
                    break

        return pawn
