from enum import Enum

class GameStates(Enum):
        INITIAL = 1
        PLAYING = 2
        ENDED = 3
    
class Directions(Enum):
        NONE = 0
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4