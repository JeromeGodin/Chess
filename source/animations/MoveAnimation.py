from source.animations.Animation import Animation
import math


class MoveAnimation(Animation):
    def __init__(self, element, element_type, original_position, target_position, duration_in_frames,
                 target_image=None):
        super().__init__(element, element_type)
        self.original_position = original_position
        self.target_position = target_position
        self.duration = duration_in_frames
        self.__frame_counter = 0
        self.__pixel_per_frame = ((original_position[0] - target_position[0]) / duration_in_frames,
                                  (original_position[1] - target_position[1]) / duration_in_frames)
        self.target_image = target_image

    def animate(self):
        if self.__frame_counter < self.duration:
            self.element.display_position = (self.element.display_position[0] - self.__pixel_per_frame[0],
                                             self.element.display_position[1] - self.__pixel_per_frame[1])

            self.__frame_counter = self.__frame_counter + 1
        else:
            self.element.display_position = self.target_position
            self.is_over = True
            self.element.currently_animated = False
