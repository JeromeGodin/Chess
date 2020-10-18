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
            Move(constants.Direction.RIGHT, 2, constants.Capture.YES, True, self._get_castling_possible_move),
            Move(constants.Direction.LEFT, 2, constants.Capture.YES, True, self._get_castling_possible_move)]

    def _get_castling_possible_move(self, move, pieces, board):
        play_direction = 1 - 2 * self.owner
        possible_move = None

        if not self.has_moved:
            valid_rook = self.get_castling_rook(move.direction.value[1], pieces, board)

            if valid_rook is not None:
                king_position = self.board_position
                valid_move = True

                for distance in range(1, move.distance + 1):
                    king_position = (self.board_position[0] + move.direction.value[0] * play_direction * distance,
                                     self.board_position[1] + move.direction.value[1] * play_direction * distance)

                    for piece in pieces:
                        if piece.board_position == king_position:
                            valid_move = False
                            break

                    if not valid_move:
                        break

                    if self._does_move_cause_check(self.owner, king_position, pieces, board):
                        valid_move = False
                        break

                if valid_move:
                    possible_move = self._get_possible_move(king_position,
                                                            board.tiles[king_position[0]][king_position[1]], False)

        return possible_move

    def get_castling_rook(self, move_direction_value, pieces, board):
        rook_position = (
            self.board_position[0], board.size[1] - 1 if move_direction_value < 0 else 0)
        rook = None

        for piece in pieces:
            if piece.board_position == rook_position and piece.owner == self.owner and not piece.has_moved:
                rook = piece
                break

        return rook
