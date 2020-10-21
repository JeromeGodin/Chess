import pygame as pg


class Button:
    def __init__(self, position, size, color, hovered_color, text, text_color, text_size, shadow_color=None,
                 hovered_shadow_color=None):
        self.position = position
        self.size = size
        self.color = color
        self.hovered_color = hovered_color
        self.text = self.__initialize_font(text, text_size, text_color)
        self.shadow_color = shadow_color
        self.hovered_shadow_color = hovered_shadow_color

    @staticmethod
    def __initialize_font(text, text_size, text_color):
        return pg.font.Font("assets\\fonts\\Montserrat\\Montserrat-Bold.ttf", text_size).render(text, True, text_color)

    def draw(self, display, hovered=False):
        radius = 10
        shadow_height = 5

        button_color = self.color if not hovered else self.hovered_color

        if self.shadow_color is not None:
            shadow_color = self.shadow_color if not hovered or \
                                                self.hovered_shadow_color is None else self.hovered_shadow_color

            # Draw the button's shadow
            pg.draw.rect(display, shadow_color,
                         pg.Rect(self.position[0], self.position[1] + self.size[1] - radius, self.size[0],
                                 shadow_height))
            pg.draw.rect(display, shadow_color,
                         pg.Rect(self.position[0] + radius, self.position[1] + self.size[1], self.size[0] - 2 * radius,
                                 shadow_height))
            pg.draw.circle(display, shadow_color,
                           (self.position[0] + radius, self.position[1] + self.size[1] - radius + shadow_height),
                           radius)
            pg.draw.circle(display, shadow_color,
                           (self.position[0] + self.size[0] - radius,
                            self.position[1] + self.size[1] - radius + shadow_height),
                           radius)

        # Draw the button's core
        pg.draw.rect(display, button_color,
                     pg.Rect(self.position[0] + radius, self.position[1], self.size[0] - 2 * radius, self.size[1]))
        pg.draw.rect(display, button_color,
                     pg.Rect(self.position[0], self.position[1] + radius, self.size[0], self.size[1] - 2 * radius))

        # Draw the button's rounded corners
        pg.draw.circle(display, button_color, (self.position[0] + radius, self.position[1] + radius), radius)
        pg.draw.circle(display, button_color, (self.position[0] + self.size[0] - radius, self.position[1] + radius),
                       radius)
        pg.draw.circle(display, button_color, (self.position[0] + radius, self.position[1] + self.size[1] - radius),
                       radius)
        pg.draw.circle(display, button_color,
                       (self.position[0] + self.size[0] - radius, self.position[1] + self.size[1] - radius), radius)

        # Draw the button's text
        display.blit(self.text, (
            self.position[0] + (self.size[0] - self.text.get_rect().width) / 2,
            self.position[1] + (self.size[1] - self.text.get_rect().height) / 2))
