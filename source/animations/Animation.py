from abc import ABC


class Animation(ABC):
    def __init__(self, element):
        self.element = element
