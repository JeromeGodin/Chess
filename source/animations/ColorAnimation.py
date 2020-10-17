from source.animations.Animation import Animation


class ColorAnimation(Animation):
    def __init__(self, element, original_color, colors, duration, frequency):
        super().__init__(element)
        self.original_color = original_color
        self.colors = colors
        self.duration = duration
        self.frequency = frequency
