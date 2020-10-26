import pygame as pg


class Window:
    def __init__(self, position, size, background_surface, buttons, parent_offset=(0, 0), click_callback=None):
        self._position = position
        self._size = size
        self._parent_offset = parent_offset
        self._click_callback = click_callback

        self.buttons = buttons
        self.window = background_surface

    def __hovered(self):
        mouse_position = pg.mouse.get_pos()
        window_position = (self._position[0] + self._parent_offset[0], self._position[1] + self._parent_offset[1])

        return window_position[0] <= mouse_position[0] < (window_position[0] + self._size[0]) and \
            window_position[1] <= mouse_position[1] < (window_position[1] + self._size[1])

    def display(self, display):
        for button in self.buttons:
            button.draw(self.window)

        display.blit(self.window, self._position)

    def click(self, event):
        response = None

        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                response = button.click(event)

                if response is not None:
                    break

            if response is None and self._click_callback is not None:
                if self.__hovered():
                    response = self._click_callback()

        return response
