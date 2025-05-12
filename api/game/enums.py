from django.db.models import TextChoices

class GameStatus(TextChoices):
    WAITING = 'waiting', 'Waiting'
    IN_PROGRESS = 'in_progress', 'In Progress'
    FINISHED = 'finished', 'Finished'


class GameMode(TextChoices):
    PVP = 'pvp', 'Player vs Player'
    PVB = 'pvb', 'Player vs Bot'
    BVB = 'bvb', 'Bot vs Bot'


class BotDifficulty(TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'
