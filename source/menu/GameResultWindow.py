import math
import pygame as pg
from source.game.GameSettings import GameResult
from source.menu.Button import Button
from source.menu.MenuConstants import GameResultResponse
from source.menu.Window import Window


class GameResultWindow(Window):
    def __init__(self, position, size, result, color, parent_offset=(0, 0), click_callback=None):
        self._result = result
        self._color = color

        super().__init__(position, size, self.__initialize_game_result_window_background(size, result, color),
                         self.__initialize_game_result_window_buttons(position, size), parent_offset, click_callback)

    @staticmethod
    def __initialize_game_result_window_background(size, result, color):
        header_height = 100
        result_text_color = (255, 255, 255, 255)
        finish_text_color = (220, 220, 220, 255)

        background_image = pg.image.load('assets\\images\\result-background-' + color.name.lower() + '.png')
        result_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Black.ttf", 32)
        finish_font = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Bold.ttf", 18)

        window_background = pg.Surface(size, pg.SRCALPHA)

        if result[0] == GameResult.VICTORY:
            background_color = (133, 169, 78, 255)
            result_text = result_font.render('You Won!', True, result_text_color)
            finish_text = finish_font.render('by ' + result[1].name.lower().capitalize(),
                                             True,
                                             finish_text_color)
        elif result[0] == GameResult.DRAW:
            background_color = (102, 100, 99, 255)
            result_text = result_font.render('Draw', True, result_text_color)
            finish_text = finish_font.render('by ' + result[1].name.lower().capitalize().replace('_', ' '),
                                             True,
                                             finish_text_color)
        else:
            background_color = (102, 100, 99, 255)
            result_text = result_font.render('You Lost', True, result_text_color)
            finish_text = finish_font.render('by ' + result[1].name.lower().capitalize(),
                                             True,
                                             finish_text_color)

        window_background.blit(background_image, (0, 0))

        pg.draw.rect(window_background, background_color, pg.Rect(0, 0, size[0], header_height))
        pg.draw.polygon(window_background, background_color, (
            (int(math.floor((size[0] - 100) / 2)), header_height), (int(math.floor(size[0] / 2)), header_height + 20),
            (int(math.floor((size[0] + 100) / 2)), header_height)))

        window_background.blit(result_text, (int(math.floor((size[0] - result_text.get_rect().width) / 2)), 20))
        window_background.blit(finish_text, (
            int(math.floor((size[0] - finish_text.get_rect().width) / 2)), 20 + result_text.get_rect().height))

        return window_background

    def __initialize_game_result_window_buttons(self, parent_offset, size):
        button_color = (255, 165, 0, 255)
        hovered_button_color = (255, 186, 57, 255)
        button_shadow_color = (155, 101, 0, 255)
        hovered_button_shadow_color = (198, 128, 0, 255)
        text_color = (255, 255, 255, 255)
        button_size = (250, 50)
        button_horizontal_pos = int(math.floor((size[0] - button_size[0]) / 2))

        return [
            Button((button_horizontal_pos, 130), button_size, button_color, hovered_button_color, 'Rematch', text_color,
                   18, self.__rematch_button_click, button_shadow_color, hovered_button_shadow_color,
                   parent_offset),
            Button((button_horizontal_pos, 200), button_size, button_color, hovered_button_color, 'Review Game',
                   text_color, 18, self.__review_button_click, button_shadow_color, hovered_button_shadow_color,
                   parent_offset),
            Button((button_horizontal_pos, 330), button_size, button_color, hovered_button_color, 'Back To Main Menu',
                   text_color, 18, self.__menu_button_click, button_shadow_color, hovered_button_shadow_color,
                   parent_offset)]

    @staticmethod
    def __rematch_button_click():
        return GameResultResponse.REMATCH

    @staticmethod
    def __review_button_click():
        return GameResultResponse.REVIEW

    @staticmethod
    def __menu_button_click():
        return GameResultResponse.MENU
