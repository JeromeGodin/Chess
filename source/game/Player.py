import math
from source.pieces.Bishop import Bishop
from source.pieces.King import King
from source.pieces.Knight import Knight
from source.pieces.Pawn import Pawn
from source.pieces.Queen import Queen
from source.pieces.Rook import Rook


class Player:
    def __init__(self, number, color, board_size, display_size, tile_size, horizontal_offset, vertical_offset):
        self.number = number
        self.color = color
        self.pieces = self.__initialize_pieces(number, board_size, display_size, tile_size, horizontal_offset,
                                               vertical_offset, color)

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
