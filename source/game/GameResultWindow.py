import pygame as pg
from source.game.GameSettings import GameResult


class GameResultWindow:
    def __init__(self, size, result, color):
        self.size = size
        self.result = result
        self.result_background = self.__initialize_background(color)
        self.__initialize_fonts()
        self.window = self.__initialize_window(size, result)

    @staticmethod
    def __initialize_background(color):
        return pg.image.load('assets\\images\\result-background-' + color.name.lower() + '.png')

    def __initialize_fonts(self):
        self.result_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Black.ttf", 32)
        self.finish_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Bold.ttf", 18)

    def __initialize_window(self, size, result):
        header_height = 100
        result_text_color = (255, 255, 255, 255)
        finish_text_color = (200, 200, 200, 255)
        window = pg.Surface(size, pg.SRCALPHA)

        if result[0] == GameResult.VICTORY:
            background_color = (133, 169, 78, 255)
            result_text = self.result_font.render('You Won!', True, result_text_color)
            finish_text = self.finish_font.render('by ' + result[1].name.lower().capitalize(), True,
                                                  finish_text_color)
        elif result[0] == GameResult.DRAW:
            background_color = (102, 100, 99, 255)
            result_text = self.result_font.render('Draw', True, result_text_color)
            finish_text = self.finish_font.render('by ' + result[1].name.lower().capitalize().replace('_', ' '), True,
                                                  finish_text_color)
        else:
            background_color = (102, 100, 99, 255)
            result_text = self.result_font.render('You Lost', True, result_text_color)
            finish_text = self.finish_font.render('by ' + result[1].name.lower().capitalize(), True,
                                                  finish_text_color)

        window.blit(self.result_background, (0, 0))

        pg.draw.rect(window, background_color, pg.Rect(0, 0, size[0], header_height))
        pg.draw.polygon(window, background_color, (
            ((size[0] - 100) / 2, header_height), (size[0] / 2, header_height + 20),
            ((size[0] + 100) / 2, header_height)))

        window.blit(result_text, ((size[0] - result_text.get_rect().width) / 2, 20))
        window.blit(finish_text, ((size[0] - finish_text.get_rect().width) / 2, 20 + result_text.get_rect().height))

        return window

    def display(self, display, position):
        display.blit(self.window, position)

    def click(self):
        print('Result Window Click')
