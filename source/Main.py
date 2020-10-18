import pygame as pg
import sys
from source import ApplicationSettings as app_settings
from source.game import GameSettings as game_settings
from source.game.Game import Game


def initialize_display():
    pg.init()
    display = pg.display.set_mode(app_settings.DISPLAY_SIZE)
    pg.display.set_caption(app_settings.WINDOW_TITLE)
    pg.display.set_icon(pg.image.load(app_settings.WINDOW_ICON))

    return display


def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    display = initialize_display()
    clock = pg.time.Clock()

    # Initializing a new game
    game = Game(game_settings.PLAYER_COUNT, app_settings.DISPLAY_SIZE, game_settings.TILE_SIZE_IN_PIXELS,
                game_settings.BOARD_SIZE, game_settings.BEIGE, game_settings.GREEN, game_settings.RED,
                game_settings.POSSIBLE_MOVE_RADIUS, game_settings.POSSIBLE_CAPTURE_RADIUS,
                game_settings.POSSIBLE_MOVE_COLOR, game_settings.POSSIBLE_CAPTURE_WIDTH,
                game_settings.PROMOTION_WINDOW_COLOR, game_settings.PROMOTION_WINDOW_HOVER_COLOR)

    game.start()

    # Main game loop
    while True:
        # Check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                game.click(event)

            if event.type == pg.MOUSEBUTTONUP:
                game.release_click(event)

        # Update the position of the piece being dragged
        game.update_selected_piece_position()

        # Refresh the display
        game.update_screen()
        display.blit(game.screen, (0, 0))

        pg.display.update()

        # Limit the FPS to MAX_FRAME_PER_SECOND
        clock.tick(app_settings.MAX_FRAME_PER_SECOND)


if __name__ == "__main__":
    main()
