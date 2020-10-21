import pygame as pg
from source.game.GameSettings import GameResult
from source.menu.Button import Button
from source.menu.MenuConstants import GameResultResponse


class GameResultWindow:
    def __init__(self, position, size, result, color):
        self.position = position
        self.size = size
        self.result = result
        self.result_background = self.__initialize_background(color)
        self.__initialize_fonts()
        self.__initialize_buttons()
        self.window = self.__initialize_window(size, result)

    @staticmethod
    def __initialize_background(color):
        return pg.image.load('assets\\images\\result-background-' + color.name.lower() + '.png')

    def __initialize_fonts(self):
        self.result_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Black.ttf", 32)
        self.finish_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Bold.ttf", 18)

    def __initialize_buttons(self):
        button_color = (255, 165, 0, 255)
        hovered_button_color = (255, 186, 57, 255)
        button_shadow_color = (155, 101, 0, 255)
        hovered_button_shadow_color = (198, 128, 0, 255)
        text_color = (255, 255, 255, 255)

        self.rematch_button = Button((25, 160), (250, 50), button_color, hovered_button_color, 'Rematch', text_color,
                                     18, button_shadow_color, hovered_button_shadow_color)
        self.review_button = Button((25, 230), (250, 50), button_color, hovered_button_color, 'Review Game', text_color,
                                    18, button_shadow_color, hovered_button_shadow_color)
        self.menu_button = Button((25, 330), (250, 50), button_color, hovered_button_color, 'Back To Main Menu',
                                  text_color, 18, button_shadow_color, hovered_button_shadow_color)

    def __initialize_window(self, size, result):
        header_height = 100
        result_text_color = (255, 255, 255, 255)
        finish_text_color = (220, 220, 220, 255)
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

    def __is_button_hovered(self, button):
        mouse_position = pg.mouse.get_pos()
        button_position = (button.position[0] + self.position[0], button.position[1] + self.position[1])

        return button_position[0] <= mouse_position[0] < (button_position[0] + button.size[0]) and \
            button_position[1] <= mouse_position[1] < (button_position[1] + button.size[1])

    def display(self, display):
        display.blit(self.window, self.position)

        self.rematch_button.draw(self.window, self.__is_button_hovered(self.rematch_button))
        self.review_button.draw(self.window, self.__is_button_hovered(self.review_button))
        self.menu_button.draw(self.window, self.__is_button_hovered(self.menu_button))

    def click(self, event):
        game_result_response = None

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.__is_button_hovered(self.rematch_button):
                game_result_response = GameResultResponse.REMATCH
            elif self.__is_button_hovered(self.review_button):
                game_result_response = GameResultResponse.REVIEW
            elif self.__is_button_hovered(self.menu_button):
                game_result_response = GameResultResponse.MENU

        return game_result_response
