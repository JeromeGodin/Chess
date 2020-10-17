from source.animations.Animation import Animation


class MoveAnimation(Animation):
    def __init__(self, element, original_location, target_location, duration):
        super().__init__(element)
        self.original_location = original_location
        self.target_location = target_location
        self.duration = duration
