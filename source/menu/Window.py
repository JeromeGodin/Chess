import pygame as pg


class Window:
    def __init__(self, position, size, background_surface, buttons, parent_offset=(0, 0)):
        self._position = position
        self._size = size
        self._parent_offset = parent_offset

        self.buttons = buttons
        self.window = background_surface

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

        return response
