import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchAvailableGames } from '../middlewares/gameMiddleware'
import { AppDispatch, RootState } from '../store'

interface IProps {
  onSelect: (gameId: string) => void
  gameId?: string
}

const GameList: React.FC<IProps> = ({ onSelect, gameId }: IProps) => {
  const dispatch = useDispatch<AppDispatch>()
  const { loading, error, games } = useSelector((state: RootState) => state.game)

  useEffect(() => {
    dispatch(fetchAvailableGames())
  }, [dispatch])

  return (
    <div className="flex flex-col items-center">
      <h5 className="h5">Available Games</h5>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {games && games.length > 0 ? (
        games.map((game) => (
          <button
            key={game.id}
            className={`btn my-3 ${gameId === game.id && 'selected'}`}
            onClick={() => onSelect(game.id)}
          >
            {game.creator}
          </button>
        ))
      ) : (
        <p>No available games</p>
      )}
    </div>
  )
}

export default GameList
