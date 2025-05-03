import { AppDispatch } from '../store'
import axios from 'axios'
import { setGameState, setWinner } from '../reducers/gameSlice'
import { BotDifficulty, GameMode, GameStatus } from '../utils/enums'

export const startGame =
  (gameMode: GameMode, botDifficulty?: BotDifficulty) => async (dispatch: AppDispatch) => {
    try {
      const response = await axios.post('/api/start-game', {
        gameMode,
        botDifficulty,
      })
      const { gameId, board, currentTurn } = response.data
      dispatch(
        setGameState({
          gameId,
          board,
          currentTurn,
          currentGameStatus: GameStatus.IN_PROGRESS,
          moveHistory: [],
        })
      )
    } catch (error) {
      console.error('Failed to start game:', error)
    }
  }

export const makeMove =
  (gameId: string, row: number, direction: 'L' | 'R') => async (dispatch: AppDispatch) => {
    try {
      const response = await axios.post(`/api/make-move`, {
        gameId,
        row,
        direction,
      })
      const { board, currentTurn, winner } = response.data
      dispatch(
        setGameState({
          gameId,
          board,
          currentTurn,
          currentGameStatus: winner ? GameStatus.COMPLETED : GameStatus.IN_PROGRESS,
          moveHistory: [], // Update this if the API returns move history
        })
      )
      if (winner) {
        dispatch(setWinner(winner))
      }
    } catch (error) {
      console.error('Failed to make move:', error)
    }
  }
