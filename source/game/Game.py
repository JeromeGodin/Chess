import pygame as pg
import math
from source.game.GameSettings import GameStatus
from source.game.GameSettings import GameResult
from source.game.GameSettings import GameFinish
from source.game.History import GameHistory
from source.pieces import Constants as constants
from source.animations.ColorAnimation import ColorAnimation
from source.animations.MoveAnimation import MoveAnimation
from source.animations import AnimationSettings as anim_settings
from source.pieces.Bishop import Bishop
from source.pieces.Knight import Knight
from source.pieces.Queen import Queen
from source.pieces.Rook import Rook


class Game:
    def __init__(self, board, players, display_size, possible_move_radius, possible_capture_radius,
                 possible_move_color, possible_capture_width, promotion_window_color, promotion_window_hover_color,
                 hovered_tile_border_width, max_moves=50):
        self.board = board
        self.players = players
        self.screen = self.__initialize_screen(display_size)
        self.__initialized_sounds()
        self.__initialize_font()

        self.promotion_window_color = promotion_window_color
        self.promotion_window_hover_color = promotion_window_hover_color
        self.__promoting_piece = None
        self.__promotion_in_progress = False
        self.__promotion_window_position = None
        self.__promotion_pieces_positions = []

        self.player_count = len(players)
        self.active_player = 0 if self.players[0].color == constants.Color.WHITE else 1
        self.status = GameStatus.NOT_STARTED
        self.result = None

        self.max_moves = max_moves
        self.move_counter = 0

        self.possible_move_radius = possible_move_radius
        self.possible_move_color = possible_move_color
        self.possible_capture_radius = possible_capture_radius
        self.possible_capture_width = possible_capture_width
        self.hovered_tile_border_width = hovered_tile_border_width

        self.dragged_piece = None
        self.selected_piece = None
        self.possible_moves = []

        self.color_animations = []
        self.move_animations = []

        self.last_move = None
        self.move_history = GameHistory(self.board)

    @staticmethod
    def __initialize_screen(size):
        return pg.Surface(size, pg.SRCALPHA)

    def __initialized_sounds(self):
        self.move_sound = pg.mixer.Sound("assets\\sounds\\move.wav")
        self.capture_sound = pg.mixer.Sound("assets\\sounds\\capture.wav")
        self.check_sound = pg.mixer.Sound("assets\\sounds\\check.wav")
        self.castle_sound = pg.mixer.Sound("assets\\sounds\\castle.wav")
        self.promotion_sound = pg.mixer.Sound("assets\\sounds\\promote.wav")
        self.illegal_sound = pg.mixer.Sound("assets\\sounds\\illegal.wav")
        self.game_start_sound = pg.mixer.Sound("assets\\sounds\\game-start.wav")
        self.game_end_sound = pg.mixer.Sound("assets\\sounds\\game-end.wav")

    def __initialize_font(self):
        self.font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Black.ttf", 18)
        self.rank_names = []
        self.file_names = []

        is_white = False
        for rank in self.board.ranks:
            self.rank_names.append(
                self.font.render(rank, True, self.board.white_color if is_white else self.board.black_color))
            is_white = not is_white

        is_white = True
        for file in self.board.files:
            self.file_names.append(
                self.font.render(file, True, self.board.white_color if is_white else self.board.black_color))
            is_white = not is_white

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

    def __move_selected_piece(self, tile, pieces, is_animated):
        is_check = False
        captured_piece = None
        target_image_position = None
        castling = False
        original_board_position = self.selected_piece.board_position

        self.last_move = (
            self.board.tiles[self.selected_piece.board_position[0]][self.selected_piece.board_position[1]],
            tile)

        # Castling
        if self.selected_piece.piece == constants.Type.KING and abs(
                self.selected_piece.board_position[1] - tile.board_position[1]) > 1:
            move_direction_value = int(
                math.floor((self.selected_piece.board_position[1] - tile.board_position[1]) / abs(
                    self.selected_piece.board_position[1] - tile.board_position[1])))
            rook = self.selected_piece.get_castling_rook(move_direction_value, pieces, self.board)
            rook_tile = self.board.tiles[rook.board_position[0]][
                tile.board_position[1] + move_direction_value]

            rook.move(rook_tile, False)
            self.__add_animation(
                MoveAnimation(rook, type(rook), rook.display_position,
                              rook_tile.display_position, anim_settings.PIECE_MOVE_DURATION, None,
                              anim_settings.PIECE_MOVE_ERASE_TARGET), self.move_animations)

            castling = True
        # Mark as en passant
        elif self.selected_piece.piece == constants.Type.PAWN and abs(
                self.selected_piece.board_position[0] - tile.board_position[0]) > 1:
            self.selected_piece.could_get_captured_en_passant = True
        # Check if pawn is capturing en passant
        elif self.selected_piece.piece == constants.Type.PAWN and \
                abs(self.selected_piece.board_position[0] - tile.board_position[0]) == 1 and \
                abs(self.selected_piece.board_position[1] - tile.board_position[1]) == 1:
            is_en_passant = True

            for piece in pieces:
                if piece.board_position == tile.board_position:
                    is_en_passant = False
                    break

            if is_en_passant:
                captured_piece = self.selected_piece.get_en_passant_pawn(
                    tile.board_position[1] - self.selected_piece.board_position[1], pieces)
                target_image_position = captured_piece.display_position

        # Check for capture
        for piece in pieces:
            if piece.board_position == tile.board_position:
                captured_piece = piece
                break

        if captured_piece is not None:
            captured_piece.captured = True

        # Move and animate piece if necessary
        self.selected_piece.move(tile, not is_animated)

        if is_animated:
            self.__add_animation(
                MoveAnimation(self.selected_piece, type(self.selected_piece), self.selected_piece.display_position,
                              tile.display_position, anim_settings.PIECE_MOVE_DURATION,
                              captured_piece.image if captured_piece is not None else None, target_image_position,
                              anim_settings.PIECE_MOVE_ERASE_TARGET), self.move_animations)

        # Check for promotions
        if self.selected_piece.piece == constants.Type.PAWN and self.selected_piece.board_position[0] == (
                (self.board.size[0] - 1) * self.active_player):
            self.__start_promotion(self.selected_piece)

        # Check for checks
        for player in self.players:
            if player.number != self.active_player:
                is_check = is_check or player.get_is_in_check(pieces, self.board)

        # Play the appropriate sound if it is not a check
        if not is_check:
            if not castling:
                if captured_piece is not None:
                    pg.mixer.Sound.play(self.capture_sound)
                else:
                    pg.mixer.Sound.play(self.move_sound)
            else:
                pg.mixer.Sound.play(self.castle_sound)
        else:
            pg.mixer.Sound.play(self.check_sound)

        # Record the move
        self.move_history.record_move(self.selected_piece, original_board_position, captured_piece is not None,
                                      is_check, pieces)

        # Increment or reset the move counter
        if self.selected_piece.piece != constants.Type.PAWN and captured_piece is None:
            self.move_counter = self.move_counter + 1
        else:
            self.move_counter = 0

        # Pass the turn
        self.possible_moves = []

        if not self.__promotion_in_progress:
            self.__pass_turn()

    def __display_ranks(self):
        index = 0

        for rank in self.rank_names:
            self.screen.blit(rank, (self.board.tiles[index][0].display_position[0] + 5,
                                    self.board.tiles[index][0].display_position[1]))
            index = index + 1

    def __display_files(self):
        index = 0

        for file in self.file_names:
            self.screen.blit(file, (self.board.tiles[self.board.size[1] - 1][index].display_position[0] + 85,
                                    self.board.tiles[self.board.size[1] - 1][index].display_position[1] + 75))
            index = index + 1

    def __run_background_animation(self):
        for animation in self.color_animations:
            animation.animate()
            pg.draw.rect(self.screen, animation.element.color, animation.element.background)

        self.__clear_animations(self.color_animations)

    def __run_piece_animation(self):
        for animation in self.move_animations:
            animation.animate()
            if animation.display_target_image:
                self.screen.blit(animation.target_image, animation.target_image_position)
            self.screen.blit(animation.element.image, animation.element.display_position)

        self.__clear_animations(self.move_animations)

    @staticmethod
    def __clear_animations(animations):
        for animation in animations:
            if animation.is_over:
                animations.remove(animation)

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
            new_animation.element.currently_animated = True

    def __pass_turn(self):
        self.active_player = (self.active_player + 1) % self.player_count
        for piece in self.players[self.active_player].pieces:
            if piece.piece == constants.Type.PAWN:
                piece.could_get_captured_en_passant = False

    def __start_promotion(self, piece):
        self.__promoting_piece = piece
        self.__promotion_in_progress = True

        if not piece.currently_animated:
            self.__promotion_window_position = self.selected_piece.display_position
        else:
            for animation in self.move_animations:
                if animation.element == piece:
                    self.__promotion_window_position = animation.target_position
                    break

        play_direction = 1 - 2 * self.active_player
        self.__promotion_pieces_positions.append((constants.Type.QUEEN, self.__promotion_window_position,
                                                  piece.board_position))
        self.__promotion_pieces_positions.append((constants.Type.KNIGHT, (self.__promotion_window_position[0],
                                                                          self.__promotion_window_position[
                                                                              1] + play_direction *
                                                                          self.board.tiles[0][0].tile_size),
                                                  (piece.board_position[0] + play_direction, piece.board_position[1])))
        self.__promotion_pieces_positions.append((constants.Type.ROOK, (self.__promotion_window_position[0],
                                                                        self.__promotion_window_position[
                                                                            1] + play_direction * 2 *
                                                                        self.board.tiles[0][0].tile_size), (
                                                      piece.board_position[0] + 2 * play_direction,
                                                      piece.board_position[1])))
        self.__promotion_pieces_positions.append((constants.Type.BISHOP, (self.__promotion_window_position[0],
                                                                          self.__promotion_window_position[
                                                                              1] + play_direction * 3 *
                                                                          self.board.tiles[0][0].tile_size), (
                                                      piece.board_position[0] + 3 * play_direction,
                                                      piece.board_position[1])))

    def __end_promotion(self, piece_choice):
        pieces = []
        is_check = False

        self.__promote_piece(self.__promoting_piece, piece_choice)

        for player in self.players:
            pieces.extend(player.pieces)

        for player in self.players:
            if player.number != self.active_player:
                is_check = is_check or player.get_is_in_check(pieces, self.board)

        pg.mixer.Sound.play(self.check_sound if is_check else self.promotion_sound)

        self.__promoting_piece = None
        self.__promotion_window_position = None
        self.__promotion_pieces_positions = []
        self.__promotion_in_progress = False

        self.__pass_turn()

    def __display_promotion_window(self):
        pg.draw.rect(self.screen, self.promotion_window_color,
                     pg.Rect(self.__promotion_window_position[0],
                             self.__promotion_window_position[1] - self.active_player * 3 * self.board.tiles[0][
                                 0].tile_size,
                             self.board.tiles[0][0].tile_size,
                             self.board.tiles[0][0].tile_size * 4))

        mouse_tile_position = self.__get_tile_from_position(pg.mouse.get_pos()).display_position

        for position in self.__promotion_pieces_positions:
            if position[1] == mouse_tile_position:
                pg.draw.rect(self.screen, self.promotion_window_hover_color,
                             pg.Rect(position[1][0],
                                     position[1][1],
                                     self.board.tiles[0][0].tile_size,
                                     self.board.tiles[0][0].tile_size))
                break

        for image in self.players[self.active_player].promotion_images:
            for piece in self.__promotion_pieces_positions:
                if piece[0] == image[0]:
                    self.screen.blit(image[1], piece[1])

    def __promote_piece(self, piece, piece_choice=constants.Type.QUEEN):
        new_piece = None
        self.players[piece.owner].pieces.remove(piece)

        if piece_choice == constants.Type.QUEEN:
            new_piece = Queen(piece.owner, piece.board_position, piece.display_position, piece.color)
            self.players[piece.owner].pieces.append(new_piece)
        elif piece_choice == constants.Type.KNIGHT:
            new_piece = Knight(piece.owner, piece.board_position, piece.display_position, piece.color)
            self.players[piece.owner].pieces.append(new_piece)
        elif piece_choice == constants.Type.ROOK:
            new_piece = Rook(piece.owner, piece.board_position, piece.display_position, piece.color)
            self.players[piece.owner].pieces.append(new_piece)
        elif piece_choice == constants.Type.BISHOP:
            new_piece = Bishop(piece.owner, piece.board_position, piece.display_position, piece.color)
            self.players[piece.owner].pieces.append(new_piece)

        return new_piece

    def __handle_game_click(self, event):
        if not self.__promotion_in_progress:
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
                                self.__move_selected_piece(target_tile, pieces, True)
                                break

                    self.possible_moves = []
                    self.selected_piece = None
        else:
            for position in self.__promotion_pieces_positions:
                if self.__is_position_in_tile(event.pos, self.board.tiles[position[2][0]][position[2][1]]):
                    self.__end_promotion(position[0])
                    break

    def __handle_game_release_click(self, event):
        if not self.__promotion_in_progress:
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

                            self.__move_selected_piece(target_tile, pieces, False)
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
                                            ColorAnimation(tile, type(tile), tile.color,
                                                           [tile.color, self.board.illegal_color],
                                                           anim_settings.TILE_FLASHING_DURATION,
                                                           anim_settings.TILE_FLASHING_FREQUENCY),
                                            self.color_animations)
                                        break

                    self.dragged_piece = None

    def __check_if_game_is_over(self):
        pieces = []
        for player in self.players:
            pieces.extend(player.pieces)

        if self.__check_if_checkmate(pieces):
            self.move_history.add_checkmate_mark()
            self.status = GameStatus.OVER
        elif self.__check_if_stalemate(pieces) or self.__check_if_repetition() or \
                self.__check_if_max_moves() or self.__check_if_insufficient_material():
            self.status = GameStatus.OVER

        if self.status == GameStatus.OVER:
            pg.mixer.Sound.play(self.game_end_sound)

    def __check_if_checkmate(self, pieces):
        checkmated_player = None
        for player in self.players:
            if player.get_is_in_checkmate(pieces, self.board):
                checkmated_player = player
                break

        if checkmated_player is not None:
            self.result = (
                GameResult.VICTORY if checkmated_player.number != 0 else GameResult.DEFEAT, GameFinish.CHECKMATE)

        return checkmated_player is not None

    def __check_if_stalemate(self, pieces):
        stalemated_player = None
        for player in self.players:
            if player.get_is_in_stalemate(pieces, self.board):
                stalemated_player = player
                break

        if stalemated_player is not None:
            self.result = (GameResult.DRAW, GameFinish.STALEMATE)

        return stalemated_player is not None

    def __check_if_repetition(self):
        repetition = self.move_history.check_for_repetition()

        if repetition:
            self.result = (GameResult.DRAW, GameFinish.REPETITION)

        return repetition

    def __check_if_max_moves(self):
        if self.move_counter >= self.max_moves:
            self.result = (GameResult.DRAW, GameFinish.MAX_MOVES)

        return self.move_counter >= self.max_moves

    def __check_if_insufficient_material(self):
        insufficient_material = True

        for player in self.players:
            if player.get_has_enough_material():
                insufficient_material = False
                break

        if insufficient_material:
            self.result = (GameResult.DRAW, GameFinish.INSUFFICIENT_MATERIAL)

        return insufficient_material

    def update_screen(self):
        # self.screen.fill((0, 0, 0, 255))

        for tile_row in self.board.tiles:
            for tile in tile_row:
                if not tile.currently_animated:
                    pg.draw.rect(self.screen, tile.color, tile.background)

        if self.last_move is not None:
            pg.draw.rect(self.screen, self.board.last_move_color, self.last_move[0].background)
            pg.draw.rect(self.screen, self.board.last_move_color, self.last_move[1].background)

        self.__display_ranks()
        self.__display_files()

        self.__run_background_animation()

        for player in self.players:
            for piece in player.pieces:
                if piece is not self.dragged_piece and not piece.captured and not piece.currently_animated:
                    self.screen.blit(piece.image, piece.display_position)

        for move in self.possible_moves:
            if move[2]:
                pg.draw.circle(self.screen, self.possible_move_color, move[1], self.possible_capture_radius,
                               self.possible_capture_width)
            else:
                pg.draw.circle(self.screen, self.possible_move_color, move[1], self.possible_move_radius)

        self.__run_piece_animation()

        if self.dragged_piece is not None:
            hovered_tile = self.__get_tile_from_position(pg.mouse.get_pos())
            pg.draw.rect(self.screen, self.possible_move_color,
                         pg.Rect(hovered_tile.display_position[0], hovered_tile.display_position[1],
                                 hovered_tile.tile_size,
                                 hovered_tile.tile_size), self.hovered_tile_border_width)

            self.screen.blit(self.dragged_piece.image, self.dragged_piece.display_position)

        if self.__promotion_in_progress:
            self.__display_promotion_window()

    def click(self, event):
        if self.status == GameStatus.IN_PROGRESS:
            self.__handle_game_click(event)
            self.__check_if_game_is_over()

    def release_click(self, event):
        if self.status == GameStatus.IN_PROGRESS:
            self.__handle_game_release_click(event)
            self.__check_if_game_is_over()

    def update_selected_piece_position(self):
        if self.dragged_piece is not None:
            position = pg.mouse.get_pos()
            self.dragged_piece.display_position = (
                position[0] - (self.board.tiles[0][0].tile_size / 2),
                position[1] - (self.board.tiles[0][0].tile_size / 2))

    def start(self):
        self.status = GameStatus.IN_PROGRESS
        pg.mixer.Sound.play(self.game_start_sound)
