import React from 'react'
import { GameMode } from '../utils/enums'

interface IProps {
  onSelect: (mode: GameMode) => void
  mode?: GameMode
}

const GameModeSelector: React.FC<IProps> = ({ onSelect: onSelect, mode }: IProps) => {
  return (
    <div className="flex flex-col items-center">
      <h5 className="h5">Game Mode</h5>

      <button
        className={`btn my-3 ${mode === GameMode.PVP && 'selected'}`}
        onClick={() => onSelect(GameMode.PVP)}
      >
        Player vs Player
      </button>
      <button
        className={`btn my-3 ${mode === GameMode.PVB && 'selected'}`}
        onClick={() => onSelect(GameMode.PVB)}
      >
        Player vs Bot
      </button>
      <button
        className={`btn my-3 ${mode === GameMode.BVB && 'selected'}`}
        onClick={() => onSelect(GameMode.BVB)}
      >
        Bot vs Bot
      </button>
    </div>
  )
}

export default GameModeSelector
