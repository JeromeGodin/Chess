from source.animations.Animation import Animation


class ColorAnimation(Animation):
    def __init__(self, element, element_type, original_color, colors, duration_in_frames, frequency_in_frames):
        super().__init__(element, element_type)
        self.original_color = original_color
        self.colors = colors
        self.duration = duration_in_frames
        self.frequency = frequency_in_frames
        self.__frame_counter = 0
        self.__color_counter = 0

    def animate(self):
        if self.__frame_counter < self.duration:
            if self.__frame_counter % self.frequency == 0:
                self.element.color = self.colors[self.__color_counter]
                self.__color_counter = (self.__color_counter + 1) % len(self.colors)

            self.__frame_counter = self.__frame_counter + 1
        else:
            self.element.color = self.original_color
            self.is_over = True

    def reset(self):
        self.__frame_counter = 0
        self.__color_counter = 0
