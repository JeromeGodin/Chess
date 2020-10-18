import math
import pygame as pg
from source.pieces.Bishop import Bishop
from source.pieces.King import King
from source.pieces.Knight import Knight
from source.pieces.Pawn import Pawn
from source.pieces.Queen import Queen
from source.pieces.Rook import Rook
from source.pieces import Constants as constants


class Player:
    def __init__(self, number, color, board_size, display_size, tile_size, horizontal_offset, vertical_offset):
        self.number = number
        self.color = color
        self.pieces = self.__initialize_pieces(number, board_size, display_size, tile_size, horizontal_offset,
                                               vertical_offset, color)
        self.promotion_images = self.__initialize_promotion_images()

    @staticmethod
    def __initialize_pieces(player, board_size, display_size, tile_size, horizontal_offset, vertical_offset,
                            color):
        pieces = []

        # Positions
        player_pawns_y_position = vertical_offset + int(math.floor((display_size[1] - tile_size) / 2)) + (
                (1 - 2 * player) * int(math.floor((display_size[1] - 3 * tile_size) / 2)))
        player_pieces_y_position = vertical_offset + int(math.floor((display_size[1] - tile_size) / 2)) + (
                (1 - 2 * player) * int(math.floor((display_size[1] - tile_size) / 2)))

        # Pawns
        for pawn in range(board_size[1]):
            pawn_position = (horizontal_offset + pawn * tile_size, player_pawns_y_position)
            pieces.append(
                Pawn(player, (board_size[0] - 2 if not player else 1, pawn), pawn_position, color))

        # Rooks
        pieces.append(
            Rook(player, (board_size[0] - 1 if not player else 0, 0), (horizontal_offset, player_pieces_y_position),
                 color))
        pieces.append(
            Rook(player, (board_size[0] - 1 if not player else 0, board_size[1] - 1),
                 (horizontal_offset + display_size[0] - 1 * tile_size, player_pieces_y_position),
                 color))

        # Knights
        pieces.append(
            Knight(player, (board_size[0] - 1 if not player else 0, 1),
                   (horizontal_offset + tile_size, player_pieces_y_position), color))
        pieces.append(
            Knight(player, (board_size[0] - 1 if not player else 0, board_size[1] - 2),
                   (horizontal_offset + display_size[0] - 2 * tile_size, player_pieces_y_position),
                   color))

        # Bishops
        pieces.append(
            Bishop(player, (board_size[0] - 1 if not player else 0, 2),
                   (horizontal_offset + 2 * tile_size, player_pieces_y_position), color))
        pieces.append(
            Bishop(player, (board_size[0] - 1 if not player else 0, board_size[1] - 3),
                   (horizontal_offset + display_size[0] - 3 * tile_size, player_pieces_y_position),
                   color))

        # Queen
        pieces.append(
            Queen(player, (board_size[0] - 1 if not player else 0, 3),
                  (horizontal_offset + 3 * tile_size, player_pieces_y_position), color))

        # King
        pieces.append(
            King(player, (board_size[0] - 1 if not player else 0, board_size[1] - 4),
                 (horizontal_offset + display_size[0] - 4 * tile_size, player_pieces_y_position),
                 color))

        return pieces

    def __initialize_promotion_images(self):
        promotion_images = [(constants.Type.QUEEN, pg.image.load(
            'assets\\images\\pieces\\wq100.png' if self.color == constants.Color.WHITE else
            'assets\\images\\pieces\\bq100.png')),
                            (constants.Type.KNIGHT, pg.image.load(
                                'assets\\images\\pieces\\wn100.png' if self.color == constants.Color.WHITE else
                                'assets\\images\\pieces\\bn100.png')),
                            (constants.Type.ROOK, pg.image.load(
                                'assets\\images\\pieces\\wr100.png' if self.color == constants.Color.WHITE else
                                'assets\\images\\pieces\\br100.png')),
                            (constants.Type.BISHOP, pg.image.load(
                                'assets\\images\\pieces\\wb100.png' if self.color == constants.Color.WHITE else
                                'assets\\images\\pieces\\bb100.png'))]

        return promotion_images

    def __get_possible_moves(self, pieces, board):
        possible_moves = []
        for piece in self.pieces:
            if not piece.captured:
                possible_moves.extend(piece.get_possible_moves(pieces, board))

        return possible_moves

    def get_is_in_check(self, pieces, board):
        is_in_check = False

        for piece in self.pieces:
            if piece.piece == constants.Type.KING:
                is_in_check = piece.is_attacked(pieces, board)
                break

        return is_in_check

    def get_is_in_checkmate(self, pieces, board):
        return self.get_is_in_check(pieces, board) and len(self.__get_possible_moves(pieces, board)) == 0

    def get_is_in_stalemate(self, pieces, board):
        return not self.get_is_in_check(pieces, board) and len(self.__get_possible_moves(pieces, board)) == 0
