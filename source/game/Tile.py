import pygame as pg


class Tile:
    def __init__(self, board_position, display_position, tile_size, color, border_radius):
        self.board_position = board_position
        self.display_position = display_position
        self.tile_size = tile_size
        self.color = color
        self.boarder_radius = border_radius
        self.background = self.__initialize_tile(display_position, tile_size, border_radius)
        self.currently_animated = False

    @staticmethod
    def __initialize_tile(display_position, tile_size, border_radius):
        return pg.Rect(display_position[0], display_position[1], tile_size, tile_size, border_radius=border_radius)
