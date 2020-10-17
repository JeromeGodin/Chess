from string import ascii_uppercase as letters
from source.Tile import Tile


class Board:
    def __init__(self, board_size, tile_size, white_color, black_color, red_color, horizontal_offset, vertical_offset):
        self.size = board_size
        self.ranks = [str(i) for i in range(board_size[0] + 1)]
        self.files = letters[:board_size[1]]
        self.tiles = self.__initialize_tiles(board_size, tile_size, white_color, black_color,
                                             horizontal_offset, vertical_offset)
        self.white_color = white_color
        self.black_color = black_color
        self.red_color = red_color

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
