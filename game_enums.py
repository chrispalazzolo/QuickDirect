from enum import Enum

class GameStates(Enum):
        INITIAL = 1
        PLAYING = 2
        ENDED = 3
    
class Directions(Enum):
        NONE = -1
        UP = 0
        DOWN = 180
        LEFT = 270
        RIGHT = 90