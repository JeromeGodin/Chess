from source.ApplicationSettings import MAX_FRAME_PER_SECOND
import math


TILE_FLASHING_DURATION = int(math.floor(MAX_FRAME_PER_SECOND * 1.5))
TILE_FLASHING_FREQUENCY = int(math.floor(MAX_FRAME_PER_SECOND * 0.25))

PIECE_MOVE_DURATION = int(math.floor(MAX_FRAME_PER_SECOND * 0.3))
