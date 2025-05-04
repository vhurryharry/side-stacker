import React from 'react'
import { GameEntry } from '../utils/enums'

interface IProps {
  onSelect: (entry: GameEntry) => void
  entry?: GameEntry
}

const GameEntrySelector: React.FC<IProps> = ({ onSelect, entry }: IProps) => {
  return (
    <div className="flex flex-col items-center">
      <h5 className="h5">Game Entry</h5>

      <button
        className={`btn my-3 ${entry === GameEntry.CREATE && 'selected'}`}
        onClick={() => onSelect(GameEntry.CREATE)}
      >
        Create a New Game
      </button>
      <button
        className={`btn my-3 ${entry === GameEntry.JOIN && 'selected'}`}
        onClick={() => onSelect(GameEntry.JOIN)}
      >
        Join a Game
      </button>
    </div>
  )
}

export default GameEntrySelector
