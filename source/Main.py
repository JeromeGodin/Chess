import pygame as pg
import sys
from source import ApplicationSettings as app_settings
from source.game import GameSettings as game_settings
from source.game.Game import Game
from source.game.Board import Board
from source.game.Player import Player
from source.menu.GameResultWindow import GameResultWindow
from source.pieces.Constants import Color
from source.menu import MenuConstants, GameMenu
from source.menu.MenuConstants import GameResultResponse


def initialize_display():
    pg.init()
    display = pg.display.set_mode(app_settings.DISPLAY_SIZE)
    pg.display.set_caption(app_settings.WINDOW_TITLE)
    pg.display.set_icon(pg.image.load(app_settings.WINDOW_ICON))

    return display


def get_new_game(player_color):
    board = Board(player_color, game_settings.BOARD_SIZE, game_settings.TILE_SIZE_IN_PIXELS, game_settings.BEIGE,
                  game_settings.GREEN, game_settings.RED,
                  game_settings.YELLOW)

    players = []
    player_colors = [player_color, Color.BLACK if player_color == Color.WHITE else Color.WHITE]

    for player in range(game_settings.PLAYER_COUNT):
        players.append(Player(player, player_colors[player], game_settings.BOARD_SIZE,
                              (game_settings.DISPLAY_WIDTH, game_settings.DISPLAY_HEIGHT),
                              game_settings.TILE_SIZE_IN_PIXELS))

    return Game(board, players, app_settings.DISPLAY_SIZE, game_settings.POSSIBLE_MOVE_RADIUS,
                game_settings.POSSIBLE_CAPTURE_RADIUS, game_settings.POSSIBLE_MOVE_COLOR,
                game_settings.POSSIBLE_CAPTURE_WIDTH, game_settings.PROMOTION_WINDOW_COLOR,
                game_settings.PROMOTION_WINDOW_HOVER_COLOR, game_settings.HOVERED_TILE_BORDER_WIDTH)


def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    display = initialize_display()
    clock = pg.time.Clock()
    game_result_window = None
    player_color = Color.WHITE
    game = None
    menu = GameMenu.Menu((0, 0), app_settings.DISPLAY_SIZE, app_settings.WINDOW_TITLE)

    # Main game loop
    while True:
        # Check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if game is None:
                    response = menu.click(event)

                    if response == Color.WHITE or response == Color.BLACK:
                        player_color = response
                        game = get_new_game(player_color)
                        game.start()
                elif game.status == game_settings.GameStatus.IN_PROGRESS:
                    game.click(event)
                elif game.status == game_settings.GameStatus.OVER:
                    if game_result_window is not None:
                        response = game_result_window.click(event)
                        if response == GameResultResponse.REMATCH:
                            game_result_window = None
                            player_color = Color.WHITE if player_color != Color.WHITE else Color.BLACK
                            game = get_new_game(player_color)
                            game.start()
                        elif response == GameResultResponse.MENU:
                            game_result_window = None
                            menu.reset()
                            game = None

            if event.type == pg.MOUSEBUTTONUP:
                if game is not None:
                    if game.status == game_settings.GameStatus.IN_PROGRESS:
                        game.release_click(event)

        if game is not None:
            # Refresh the game board
            game.display(display, (0, 0))

            if game.status == game_settings.GameStatus.IN_PROGRESS:
                # Update the position of the piece being dragged
                game.update_selected_piece_position()
            elif game.status == game_settings.GameStatus.OVER:
                if game_result_window is None:
                    game_result_window = GameResultWindow(MenuConstants.GAME_RESULT_WINDOW_POSITION,
                                                          MenuConstants.GAME_RESULT_WINDOW_SIZE,
                                                          game.result,
                                                          player_color)

                game_result_window.display(display)
        else:
            menu.display(display)

        # Refresh the display
        pg.display.update()

        # Limit the FPS to MAX_FRAME_PER_SECOND
        clock.tick(app_settings.MAX_FRAME_PER_SECOND)


if __name__ == "__main__":
    main()
