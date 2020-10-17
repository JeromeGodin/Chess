from abc import ABC


class Animation(ABC):
    def __init__(self, element, element_type):
        self.element = element
        self.element_type = element_type
        self.is_over = False

    def animate(self):
        raise NotImplementedError
