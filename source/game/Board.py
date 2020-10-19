import numpy as np
from string import ascii_lowercase as letters
from source.game.Tile import Tile
from source.pieces.Constants import Color


class Board:
    def __init__(self, player_color, board_size, tile_size, white_color, black_color, illegal_color, last_move_color,
                 horizontal_offset, vertical_offset):
        self.size = board_size
        self.ranks = self.__initialize_ranks(player_color, board_size)
        self.files = self.__initialize_files(player_color, board_size)
        self.tiles = self.__initialize_tiles(board_size, tile_size, white_color, black_color,
                                             horizontal_offset, vertical_offset)
        self.white_color = white_color
        self.black_color = black_color
        self.illegal_color = illegal_color
        self.last_move_color = last_move_color

    @staticmethod
    def __initialize_ranks(player_color, board_size):
        ranks = [str(i) for i in range(board_size[0], 0, -1)]

        if player_color == Color.BLACK:
            ranks = np.flip(ranks)

        return ranks

    @staticmethod
    def __initialize_files(player_color, board_size):
        files = []
        for letter in letters[:board_size[1]]:
            files.append(letter)

        if player_color == Color.BLACK:
            files = np.flip(files)

        return files

    @staticmethod
    def __initialize_tiles(board_size, tile_size, white_color, black_color, horizontal_offset,
                           vertical_offset):
        tiles = []
        is_white = True

        for rank in range(board_size[0]):
            tiles.append([])
            for file in range(board_size[1]):
                tiles[rank].append(Tile((rank, file),
                                        (horizontal_offset + file * tile_size, vertical_offset + rank * tile_size),
                                        tile_size, white_color if is_white else black_color, 0))

                is_white = not is_white

            is_white = not is_white

        return tiles
