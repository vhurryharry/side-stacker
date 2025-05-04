import React, { useEffect } from 'react'
import GameEntrySelector from '../components/GameEntrySelector'
import GameModeSelector from '../components/GameModeSelector'
import { BotDifficulty, GameEntry, GameMode } from '../utils/enums'
import GameList from '../components/GameList'
import BotDifficultySelector from '../components/BotDifficultySelector'

const GameSetup: React.FC = () => {
  const [entry, setEntry] = React.useState<GameEntry>()
  const [mode, setMode] = React.useState<GameMode>()
  const [difficulty, setDifficulty] = React.useState<BotDifficulty>()

  useEffect(() => {
    setMode(undefined)
    setDifficulty(undefined)
  }, [entry])

  useEffect(() => {
    setDifficulty(undefined)
  }, [mode])

  return (
    <div className="flex flex-col items-center w-max min-w-max h-1/2">
      <div className="flex flex-row items-center justify-center w-full h-full">
        <div className="flex-1 mx-8 min-w-2xs">
          <GameEntrySelector onSelect={setEntry} entry={entry} />
        </div>

        {entry && (
          <div className="flex-1 mx-8 min-w-2xs">
            {entry === GameEntry.CREATE && <GameModeSelector mode={mode} onSelect={setMode} />}
            {entry === GameEntry.JOIN && <GameList onSelect={() => {}} />}
          </div>
        )}

        {mode === GameMode.PVB && (
          <div className="flex-1 mx-8 min-w-2xs">
            <BotDifficultySelector difficulty={difficulty} onSelect={setDifficulty} />
          </div>
        )}
      </div>

      <button className="btn">Start Game</button>
    </div>
  )
}

export default GameSetup
