import { AppDispatch } from '../store'
import axios from 'axios'
import {
  apiCallFailure,
  finishApiCall,
  setGameState,
  initApiCall,
  setAvailableGames,
} from '../reducers/gameSlice'
import { BotDifficulty, GameMode } from '../utils/enums'
import { GameInfo } from '../utils/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const createGame =
  (playerName: string, gameMode: GameMode, botDifficulty?: BotDifficulty) =>
  async (dispatch: AppDispatch) => {
    dispatch(initApiCall())
    try {
      const response = await api.post('/game/create/', {
        mode: gameMode,
        difficulty: botDifficulty,
        playerName,
      })
      dispatch(
        setGameState({
          ...response.data,
          myTurn: gameMode === GameMode.BVB ? 0 : 1,
        })
      )
    } catch (error) {
      dispatch(apiCallFailure(JSON.stringify(error)))
      console.error('Failed to start game:', error)
    } finally {
      dispatch(finishApiCall())
    }
  }

export const joinGame = (playerName: string, gameId: string) => async (dispatch: AppDispatch) => {
  dispatch(initApiCall())
  try {
    const response = await api.post(`/game/${gameId}/join/`, { playerName })

    dispatch(
      setGameState({
        ...response.data,
        myTurn: -1,
      })
    )
  } catch (error) {
    dispatch(apiCallFailure(JSON.stringify(error)))
    console.error('Failed to join the game:', error)
  } finally {
    dispatch(finishApiCall())
  }
}

export const fetchAvailableGames = () => async (dispatch: AppDispatch) => {
  dispatch(initApiCall())
  try {
    const response = await api.get<{ games: GameInfo[] }>('/game/list')
    dispatch(setAvailableGames(response.data?.games || []))
  } catch (error) {
    dispatch(apiCallFailure(JSON.stringify(error)))
    console.error('Failed to load available games:', error)
  } finally {
    dispatch(finishApiCall())
  }
}
