from abc import ABC
import pygame as pg
import math
from source.pieces import Constants as constants


class Piece(ABC):
    def __init__(self, owner, board_position, display_position, color, piece, value):
        self.owner = owner
        self.board_position = board_position
        self.display_position = display_position
        self.previous_display_position = display_position
        self.image = pg.image.load('assets\\images\\pieces\\wp.png')
        self.color = color
        self.piece = piece
        self.currently_animated = False
        self.has_moved = False
        self.captured = False
        self.value = value
        self._available_moves = []

    @staticmethod
    def __is_position_in_board(position, board):
        return 0 <= position[0] < board.size[0] and 0 <= position[1] < board.size[1]

    @staticmethod
    def __get_piece_from_board_position(position, pieces):
        for piece in pieces:
            if piece.board_position == position and not piece.captured:
                return piece

        return None

    @staticmethod
    def _get_possible_move(position, tile, is_capture):
        return (position, (tile.display_position[0] + int(math.floor(tile.tile_size / 2)),
                           tile.display_position[1] + int(math.floor(tile.tile_size / 2))), is_capture)

    def _does_move_cause_check(self, attacked_player, position, pieces, board):
        captured_piece = None
        for piece in pieces:
            if piece.board_position == position:
                captured_piece = piece
                captured_piece.captured = True
                break

        board_position = self.board_position
        self.board_position = position

        is_king_in_check = False

        for piece in pieces:
            if piece.piece == constants.Type.KING and piece.owner == attacked_player:
                is_king_in_check = piece.is_attacked(pieces, board)
                break

        if captured_piece is not None:
            captured_piece.captured = False

        self.board_position = board_position

        return is_king_in_check

    def get_possible_moves(self, pieces, board):
        possible_moves = []
        attacks = self.get_attacks(pieces, board)

        for attack in attacks:
            if not self._does_move_cause_check(self.owner, attack[0], pieces, board):
                possible_moves.append(attack)

        return possible_moves

    def get_attacks(self, pieces, board, ignore_custom_moves=False):
        possible_moves = []
        play_direction = 1 - 2 * self.owner

        for move in self._available_moves:
            if move.custom_handling is None:
                if not (move.first_move_only and self.has_moved):
                    max_distance = move.distance + 1
                    for distance in range(1, max_distance):
                        target_position = (self.board_position[0] + move.direction.value[0] * distance * play_direction,
                                           self.board_position[1] + move.direction.value[1] * distance * play_direction)

                        if self.__is_position_in_board(target_position, board):
                            piece = self.__get_piece_from_board_position(target_position, pieces)
                            if piece is None:
                                if move.capture is not constants.Capture.MANDATORY:
                                    possible_moves.append(self._get_possible_move(target_position,
                                                                                  board.tiles[target_position[0]][
                                                                                      target_position[1]], False))
                            else:
                                if move.capture is not constants.Capture.NO and piece.owner != self.owner:
                                    possible_moves.append(self._get_possible_move(target_position,
                                                                                  board.tiles[target_position[0]][
                                                                                      target_position[1]], True))
                                break
                        else:
                            break
            elif not (move.first_move_only and self.has_moved) and not ignore_custom_moves:
                custom_move = move.custom_handling(move, pieces, board)
                if custom_move is not None:
                    possible_moves.append(custom_move)

        return possible_moves

    def is_attacked(self, pieces, board):
        is_attacked = False

        for piece in pieces:
            if piece.owner != self.owner and not piece.captured:
                for attack in piece.get_attacks(pieces, board, True):
                    if attack[0] == self.board_position:
                        is_attacked = True
                        break

        return is_attacked

    def move(self, tile, move_on_display):
        self.has_moved = True
        self.board_position = tile.board_position
        self.previous_display_position = tile.display_position

        if move_on_display:
            self.display_position = tile.display_position
