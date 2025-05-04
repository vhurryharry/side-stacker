import React from 'react'
import { BotDifficulty } from '../utils/enums'

interface IProps {
  onSelect: (difficulty: BotDifficulty) => void
  difficulty?: BotDifficulty
}

const BotDifficultySelector: React.FC<IProps> = ({ onSelect, difficulty }: IProps) => {
  return (
    <div className="flex flex-col items-center">
      <h5 className="h5">Difficulty</h5>

      <button
        className={`btn my-3 ${difficulty === BotDifficulty.EASY && 'selected'}`}
        onClick={() => onSelect(BotDifficulty.EASY)}
      >
        Easy
      </button>
      <button
        className={`btn my-3 ${difficulty === BotDifficulty.MEDIUM && 'selected'}`}
        onClick={() => onSelect(BotDifficulty.MEDIUM)}
      >
        Medium
      </button>
      <button
        className={`btn my-3 ${difficulty === BotDifficulty.HARD && 'selected'}`}
        onClick={() => onSelect(BotDifficulty.HARD)}
      >
        Hard
      </button>
    </div>
  )
}

export default BotDifficultySelector
