import React, { useEffect } from 'react'
import GameEntrySelector from '../components/GameEntrySelector'
import GameModeSelector from '../components/GameModeSelector'
import { BotDifficulty, GameEntry, GameMode } from '../utils/enums'
import GameList from '../components/GameList'
import BotDifficultySelector from '../components/BotDifficultySelector'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { createGame, joinGame } from '../middlewares/gameMiddleware'
import { AppDispatch, RootState } from '../store'

const GameSetup: React.FC = () => {
  const [entry, setEntry] = React.useState<GameEntry>()
  const [mode, setMode] = React.useState<GameMode>()
  const [difficulty, setDifficulty] = React.useState<BotDifficulty>()
  const [gameId, setGameId] = React.useState<string>()
  const [playerName, setPlayerName] = React.useState<string>('')

  const { id, loading } = useSelector((state: RootState) => state.game)

  const dispatch = useDispatch<AppDispatch>()
  const navigate = useNavigate()

  useEffect(() => {
    setMode(undefined)
    setDifficulty(undefined)
    setGameId(undefined)
  }, [entry])

  useEffect(() => {
    setDifficulty(undefined)
    setGameId(undefined)
  }, [mode])

  const canStart =
    (mode === GameMode.BVB || playerName) &&
    (entry === GameEntry.CREATE
      ? mode && (mode !== GameMode.PVB || difficulty)
      : entry === GameEntry.JOIN
        ? gameId
        : false)

  const startGame = () => {
    if (entry === GameEntry.CREATE) {
      dispatch(createGame(playerName!, mode!, difficulty))
    } else {
      dispatch(joinGame(playerName!, gameId!))
    }
  }

  useEffect(() => {
    if (!loading && id) {
      navigate('/game')
    }
  }, [loading, id, navigate])

  return (
    <div className="flex flex-col items-center w-max min-w-max h-1/2">
      <div className="flex flex-row items-center justify-center w-full h-full">
        <div className="flex-1 mx-8 min-w-2xs">
          <GameEntrySelector onSelect={setEntry} entry={entry} />
        </div>

        {entry && (
          <div className="flex-1 mx-8 min-w-2xs max-h-full overflow-y-auto">
            {entry === GameEntry.CREATE && <GameModeSelector mode={mode} onSelect={setMode} />}
            {entry === GameEntry.JOIN && <GameList onSelect={setGameId} gameId={gameId} />}
          </div>
        )}

        {mode === GameMode.PVB && (
          <div className="flex-1 mx-8 min-w-2xs">
            <BotDifficultySelector difficulty={difficulty} onSelect={setDifficulty} />
          </div>
        )}
      </div>

      <div>
        <input
          type="text"
          className={`text-input my-2 ${mode === GameMode.BVB && 'disabled'}`}
          value={playerName}
          disabled={mode === GameMode.BVB}
          onChange={(e) => setPlayerName(e.target.value)}
          placeholder="Player Name"
        />
      </div>
      <button
        className={`btn my-3 ${!canStart && 'disabled'}`}
        disabled={!canStart}
        onClick={startGame}
      >
        Start Game
      </button>
    </div>
  )
}

export default GameSetup
