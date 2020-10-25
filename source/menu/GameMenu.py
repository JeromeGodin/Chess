import pygame as pg
import math

from source.menu.Button import Button
from source.menu.Window import Window
from source.pieces.Constants import Color


class Menu:
    def __init__(self, position, size, title, parent_offset=(0, 0)):
        self.position = position
        self.size = size
        self.active_window = 0
        self.windows = self.__initialize_windows(position, size, parent_offset, title)
        self._parent_offset = parent_offset

    def __initialize_windows(self, position, size, parent_offset, title):
        windows = [self.__initialize_title_screen(position, size, parent_offset, title),
                   self.__initialize_color_choice_screen(position, size, parent_offset, title)]

        return windows

    @staticmethod
    def __draw_border(background_surface, size, color, border_height):
        pg.draw.rect(background_surface, color, pg.Rect(0, 0, size[0], border_height))
        pg.draw.polygon(background_surface, color, (
            (int(math.floor((size[0] - 200) / 2)), border_height), (int(math.floor(size[0] / 2)), border_height + 40),
            (int(math.floor((size[0] + 200) / 2)), border_height)))
        pg.draw.rect(background_surface, color,
                     pg.Rect(0, size[1] - border_height, size[0], border_height))
        pg.draw.polygon(background_surface, color, (
            (int(math.floor((size[0] - 200) / 2)), size[1] - border_height),
            (int(math.floor(size[0] / 2)), size[1] - border_height - 40),
            (int(math.floor((size[0] + 200) / 2)), size[1] - border_height)))

    def __draw_menu_borders(self, background_surface, size):
        self.__draw_border(background_surface, size, (0, 0, 0, 255), 100)
        self.__draw_border(background_surface, size, (240, 240, 240, 255), 85)
        self.__draw_border(background_surface, size, (133, 169, 78, 255), 80)

    def __initialize_title_screen(self, position, size, parent_offset, title):
        background_surface = pg.Surface(size, pg.SRCALPHA)
        background_surface.fill((240, 240, 240, 255))

        self.__draw_menu_borders(background_surface, size)
        text = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-ExtraBold.ttf", 72).render(title, True,
                                                                                              (0, 0, 0, 255))

        background_surface.blit(text, ((size[0] - text.get_rect().width) / 2, (size[1] - text.get_rect().height) / 2))

        return Window(position, size, background_surface, [], parent_offset, click_callback=self.__title_click)

    def __initialize_color_choice_screen(self, position, size, parent_offset, title):
        background_surface = pg.Surface(size, pg.SRCALPHA)
        background_surface.fill((240, 240, 240, 255))

        self.__draw_menu_borders(background_surface, size)
        text = pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-ExtraBold.ttf", 40).render(
            'Which color do you want to play?', True,
            (0, 0, 0, 255))

        background_surface.blit(text,
                                ((size[0] - text.get_rect().width) / 2, (size[1] - text.get_rect().height) / 2 - 200))

        button_size = (500, 100)
        button_text_size = 42
        button_horizontal_pos = int(math.floor((size[0] - button_size[0]) / 2))
        buttons = [
            Button((button_horizontal_pos, 300), button_size, (250, 250, 250, 255), (255, 255, 255, 255), 'White',
                   (0, 0, 0, 255),
                   button_text_size, self.__white_click, (149, 148, 148, 255), (194, 194, 194, 255),
                   parent_offset),
            Button((button_horizontal_pos, 430), button_size, (102, 100, 99, 255), (149, 146, 145, 255), 'Black',
                   (255, 255, 255, 255), button_text_size, self.__black_click, (47, 45, 45, 255), (95, 92, 91, 255),
                   parent_offset)]

        return Window(position, size, background_surface, buttons, parent_offset, click_callback=self.__title_click)

    def __title_click(self):
        self.active_window = 1
        return None

    @staticmethod
    def __white_click():
        return Color.WHITE

    @staticmethod
    def __black_click():
        return Color.BLACK

    def display(self, display):
        self.windows[self.active_window].display(display)

    def click(self, event):
        return self.windows[self.active_window].click(event)

    def reset(self):
        self.active_window = 0
