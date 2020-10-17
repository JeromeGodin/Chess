import pygame as pg
import sys
from source import Settings as settings
from source.game.Game import Game


def initialize_display():
    pg.init()
    display = pg.display.set_mode(settings.DISPLAY_SIZE)
    pg.display.set_caption(settings.WINDOW_TITLE)
    pg.display.set_icon(pg.image.load(settings.WINDOW_ICON))

    return display


def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    display = initialize_display()
    clock = pg.time.Clock()

    # Initializing a new game
    game = Game(settings.PLAYER_COUNT, settings.DISPLAY_SIZE, settings.TILE_SIZE_IN_PIXELS, settings.BOARD_SIZE,
                settings.BEIGE, settings.GREEN, settings.RED)

    # Main game loop
    while not game.is_over:
        # Check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                game.click(event)

            if event.type == pg.MOUSEBUTTONUP:
                game.release_click(event)

        game.update_selected_piece_position()

        # Refresh the display
        game.update_screen()
        display.blit(game.screen, (0, 0))

        pg.display.update()

        # Limit the FPS to MAX_FRAME_PER_SECOND
        clock.tick(settings.MAX_FRAME_PER_SECOND)


if __name__ == "__main__":
    main()
