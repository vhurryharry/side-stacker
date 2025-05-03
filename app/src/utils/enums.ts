export enum GameStatus {
  WAITING = 'waiting',
  IN_PROGRESS = 'in_progress',
  FINISHED = 'finished',
}

export enum BotDifficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
}

export enum GameMode {
  PVP = 'pvp', // Player vs Player
  PVB = 'pvb', // Player vs Bot
  BVB = 'bvb', // Bot vs Bot
}
