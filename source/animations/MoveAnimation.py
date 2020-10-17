from source.animations.Animation import Animation


class MoveAnimation(Animation):
    def __init__(self, element, element_type, original_location, target_location, duration_in_frames):
        super().__init__(element, element_type)
        self.original_location = original_location
        self.target_location = target_location
        self.duration = duration_in_frames
