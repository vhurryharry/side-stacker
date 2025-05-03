
from enum import Enum

class GameStatus(str, Enum):
    WAITING = 'waiting'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'

class GameMode(str, Enum):
    PVP = 'pvp'
    PVB = 'pvb'
    BVB = 'bvb'

class BotDifficulty(str, Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
