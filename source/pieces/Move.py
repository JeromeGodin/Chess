class Move:
    def __init__(self, direction, distance, capture, first_move_only):
        self.direction = direction
        self.distance = distance
        self.capture = capture
        self.first_move_only = first_move_only
