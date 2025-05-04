import { AppDispatch } from '../store'
import axios from 'axios'
import {
  apiCallFailure,
  finishApiCall,
  setGameState,
  setWinner,
  initApiCall,
  setGames,
} from '../reducers/gameSlice'
import { BotDifficulty, GameMode, GameStatus } from '../utils/enums'
import { GameInfo } from '../utils/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/game'
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const startGame =
  (gameMode: GameMode, botDifficulty?: BotDifficulty) => async (dispatch: AppDispatch) => {
    dispatch(initApiCall())
    try {
      const response = await api.post('/game/create', {
        gameMode,
        botDifficulty,
      })
      dispatch(setGameState(response.data))
    } catch (error) {
      dispatch(apiCallFailure(error as string))
      console.error('Failed to start game:', error)
    } finally {
      dispatch(finishApiCall())
    }
  }

export const makeMove =
  (gameId: string, row: number, direction: 'L' | 'R') => async (dispatch: AppDispatch) => {
    dispatch(initApiCall())
    try {
      const response = await api.post(`/game/move`, {
        gameId,
        row,
        direction,
      })
      const { game, aiMove, winner } = response.data
      dispatch(setGameState(game))
      if (winner) {
        dispatch(setWinner(winner))
      }
    } catch (error) {
      dispatch(apiCallFailure(error as string))
      console.error('Failed to make move:', error)
    } finally {
      dispatch(finishApiCall())
    }
  }

export const fetchAvailableGames = () => async (dispatch: AppDispatch) => {
  dispatch(initApiCall())
  try {
    const response = await api.get<GameInfo[]>('/game/list')
    dispatch(setGames(response.data))
  } catch (error) {
    dispatch(apiCallFailure(error as string))
    console.error('Failed to load available games:', error)
  } finally {
    dispatch(finishApiCall())
  }
}

export const joinGame = (gameId: string, playerName: string) => async (dispatch: AppDispatch) => {
  dispatch(initApiCall())
  try {
    const response = await api.post(`/game/join/${gameId}`, { player2: playerName })
    dispatch(setGameState(response.data))
  } catch (error) {
    dispatch(apiCallFailure(error as string))
    console.error('Failed to join the game:', error)
  } finally {
    dispatch(finishApiCall())
  }
}
