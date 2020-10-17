import pygame as pg
import math
from source.game.Board import Board
from source.game.Player import Player
from source.pieces import Constants as constants
from source.animations.ColorAnimation import ColorAnimation
from source.animations.MoveAnimation import MoveAnimation


class Game:
    def __init__(self, player_count, display_size, tile_size, board_size, white_color, black_color, red_color,
                 horizontal_offset=0, vertical_offset=0):
        self.board = Board(board_size, tile_size, white_color, black_color, red_color, horizontal_offset,
                           vertical_offset)
        self.players = self.__initialize_players(player_count, board_size, tile_size, horizontal_offset,
                                                 vertical_offset)
        self.screen = self.__initialize_screen(display_size)
        self.__initialized_sounds()

        self.player_count = player_count
        self.active_player = 0
        self.is_over = False

        self.dragged_piece = None
        self.selected_piece = None
        self.possible_moves = []

        self.color_animations = []
        self.move_animations = []

    @staticmethod
    def __initialize_screen(size):
        return pg.Surface(size, pg.SRCALPHA)

    @staticmethod
    def __initialize_board(display, size, tile_size, white_color, black_color):
        is_white = True

        for file in range(int(math.floor(size[0] / tile_size))):
            for rank in range(int(math.floor(size[1] / tile_size))):
                pg.draw.rect(display, white_color if is_white else black_color,
                             pg.Rect(file * tile_size, rank * tile_size,
                                     tile_size, tile_size, border_radius=0))

                is_white = not is_white

            is_white = not is_white

        return display

    @staticmethod
    def __initialize_players(player_count, board_size, tile_size, horizontal_offset, vertical_offset):
        players = []

        for player in range(player_count):
            players.append(
                Player(player, constants.Color(player), board_size,
                       (board_size[1] * tile_size, board_size[0] * tile_size),
                       tile_size, horizontal_offset, vertical_offset))

        return players

    def __initialized_sounds(self):
        self.move_sound = pg.mixer.Sound("assets\\sounds\\move.wav")
        self.capture_sound = pg.mixer.Sound("assets\\sounds\\capture.wav")
        self.check_sound = pg.mixer.Sound("assets\\sounds\\check.wav")
        self.illegal_sound = pg.mixer.Sound("assets\\sounds\\illegal.wav")

    def __clear_animations(self):
        for animation in self.color_animations:
            if animation.is_over:
                self.color_animations.remove(animation)

        for animation in self.move_animations:
            if animation.is_over:
                self.move_animations.remove(animation)

    @staticmethod
    def __is_position_in_tile(position, board_tile):
        return board_tile.display_position[0] <= position[0] < (
                board_tile.display_position[0] + board_tile.tile_size) and board_tile.display_position[1] <= \
               position[1] < (board_tile.display_position[1] + board_tile.tile_size)

    def __get_tile_from_position(self, position):
        target_tile = None

        for tile_row in self.board.tiles:
            for tile in tile_row:
                if self.__is_position_in_tile(position, tile):
                    target_tile = tile
                    break

            if target_tile is not None:
                break

        return target_tile

    def __move_piece_selected_piece(self, tile, pieces, is_animated):
        is_check = False
        captured_piece = None

        for piece in pieces:
            if piece.board_position == tile.board_position:
                captured_piece = piece
                break

        if captured_piece is not None:
            captured_piece.captured = True

        self.selected_piece.move(tile, not is_animated)

        if is_animated:
            self.__add_animation(
                MoveAnimation(self.selected_piece, type(self.selected_piece), self.selected_piece.display_position,
                              tile.display_position, 18), self.move_animations)

        for piece in pieces:
            if piece.piece == constants.Type.KING and piece.owner != self.active_player:
                if piece.is_attacked(pieces, self.board):
                    pg.mixer.Sound.play(self.check_sound)
                    is_check = True
                    break

        if not is_check:
            if captured_piece is not None:
                pg.mixer.Sound.play(self.capture_sound)
            else:
                pg.mixer.Sound.play(self.move_sound)

        self.possible_moves = []
        self.pass_turn()

    @staticmethod
    def __add_animation(new_animation, animation_list):
        is_animation_new = True

        for animation in animation_list:
            if new_animation.element_type == animation.element_type and \
                    new_animation.element.display_position == animation.element.display_position:
                animation.reset()
                is_animation_new = False
                break

        if is_animation_new:
            animation_list.append(new_animation)

    def update_screen(self):
        for animation in self.color_animations:
            animation.animate()

        for animation in self.move_animations:
            animation.animate()

        for tile_row in self.board.tiles:
            for tile in tile_row:
                pg.draw.rect(self.screen, tile.color, tile.background)

        for player in self.players:
            for piece in player.pieces:
                if piece is not self.dragged_piece and not piece.captured:
                    self.screen.blit(piece.image, piece.display_position)

        for move in self.possible_moves:
            pg.draw.circle(self.screen, (100, 100, 100, 10), move[1], 20)

        if self.dragged_piece is not None:
            self.screen.blit(self.dragged_piece.image, self.dragged_piece.display_position)

        self.__clear_animations()

    def pass_turn(self):
        self.active_player = (self.active_player + 1) % self.player_count

    def click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for piece in self.players[self.active_player].pieces:
                if not piece.captured and self.__is_position_in_tile(event.pos,
                                                                     self.board.tiles[piece.board_position[0]][
                                                                         piece.board_position[1]]):
                    self.dragged_piece = piece
                    self.selected_piece = piece
                    break

            pieces = []
            for player in self.players:
                for piece in player.pieces:
                    if not piece.captured:
                        pieces.append(piece)

            if self.dragged_piece is not None:
                self.possible_moves = self.dragged_piece.get_possible_moves(pieces, self.board)
            elif self.selected_piece is not None:
                target_tile = self.__get_tile_from_position(event.pos)

                if target_tile is not None:
                    for move in self.possible_moves:
                        if move[0] == target_tile.board_position:
                            self.__move_piece_selected_piece(target_tile, pieces, True)
                            break

                self.possible_moves = []
                self.selected_piece = None

    def release_click(self, event):
        if self.dragged_piece is not None:
            if event.type == pg.MOUSEBUTTONUP:
                target_tile = self.__get_tile_from_position(event.pos)

                if target_tile is not None:
                    is_move_valid = False

                    for move in self.possible_moves:
                        if move[0] == target_tile.board_position:
                            is_move_valid = True
                            break

                    if is_move_valid:
                        pieces = []
                        for player in self.players:
                            for piece in player.pieces:
                                if not piece.captured:
                                    pieces.append(piece)

                        self.__move_piece_selected_piece(target_tile, pieces, False)
                    else:
                        self.dragged_piece.display_position = self.dragged_piece.previous_display_position

                        pieces = []
                        for player in self.players:
                            for piece in player.pieces:
                                if not piece.captured:
                                    pieces.append(piece)

                        for piece in pieces:
                            if piece.piece == constants.Type.KING and piece.owner == self.active_player:
                                if piece.is_attacked(pieces, self.board) and \
                                        (self.possible_moves == [] or
                                         target_tile.board_position != self.selected_piece.board_position):
                                    pg.mixer.Sound.play(self.illegal_sound)
                                    tile = self.board.tiles[piece.board_position[0]][piece.board_position[1]]
                                    self.__add_animation(
                                        ColorAnimation(tile, type(tile), tile.color, [tile.color, self.board.red_color],
                                                       90, 15), self.color_animations)
                                    break

                self.dragged_piece = None

    def update_selected_piece_position(self):
        if self.dragged_piece is not None:
            position = pg.mouse.get_pos()
            self.dragged_piece.display_position = (
                position[0] - (self.board.tiles[0][0].tile_size / 2),
                position[1] - (self.board.tiles[0][0].tile_size / 2))
