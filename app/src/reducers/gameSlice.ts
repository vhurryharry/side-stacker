import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { BotDifficulty, GameMode, GameStatus } from '../utils/enums'
import { GameInfo, GameMove } from '../utils/types'

interface GameState {
  // Current game information
  id: string
  moveHistory: GameMove[]
  status: GameStatus
  mode: GameMode
  botDifficulty: BotDifficulty
  board: number[][]
  currentTurn: number
  winner: number | null
  player1: string | null
  player2: string | null

  // List of available games
  games: GameInfo[]

  // Loading and error states
  loading: boolean
  error: string | null
}

const initialState: GameState = {
  id: '',
  status: GameStatus.WAITING,
  moveHistory: [],
  mode: GameMode.PVP,
  botDifficulty: BotDifficulty.MEDIUM,
  board: Array(7).fill(Array(7).fill(0)),
  currentTurn: 1, // Player 1 starts
  winner: null,
  player1: null,
  player2: null,

  games: [],

  loading: false,
  error: null,
}

const gameSlice = createSlice({
  name: 'game',
  initialState,
  reducers: {
    startGame: (
      state,
      action: PayloadAction<{
        id: string
        mode: GameMode
        botDifficulty?: BotDifficulty
      }>
    ) => {
      state.id = action.payload.id
      state.status = GameStatus.IN_PROGRESS
      state.mode = action.payload.mode
      if (action.payload.mode === GameMode.PVB) {
        state.botDifficulty = action.payload.botDifficulty || BotDifficulty.MEDIUM
      }
      state.moveHistory = []
      state.board = Array(7).fill(Array(7).fill(0))
    },
    makeMove: (state, action: PayloadAction<{ row: number; direction: 'L' | 'R' }>) => {
      const { row, direction } = action.payload
      const board = state.board.map((r) => [...r])

      if (direction === 'L') {
        for (let col = 0; col < 7; col++) {
          if (board[row][col] === 0) {
            board[row][col] = state.currentTurn
            break
          }
        }
      } else {
        for (let col = 6; col >= 0; col--) {
          if (board[row][col] === 0) {
            board[row][col] = state.currentTurn
            break
          }
        }
      }

      state.board = board
      state.moveHistory.push({ row, direction, player: state.currentTurn })
      state.currentTurn = -state.currentTurn
    },
    setGameState: (
      state,
      action: PayloadAction<{
        id: string
        board: number[][]
        currentTurn: number
        status: GameStatus
        mode: GameMode
        botDifficulty: BotDifficulty
        player1: string | null
        player2: string | null
        moveHistory: GameMove[]
      }>
    ) => {
      state.id = action.payload.id
      state.board = action.payload.board || state.board
      state.currentTurn = action.payload.currentTurn
      state.status = action.payload.status
      state.mode = action.payload.mode
      state.botDifficulty = action.payload.botDifficulty
      state.player1 = action.payload.player1
      state.player2 = action.payload.player2
      state.moveHistory = action.payload.moveHistory || state.moveHistory
    },
    setWinner: (state, action: PayloadAction<number>) => {
      state.winner = action.payload
      state.status = GameStatus.FINISHED
    },
    resetGame: () => initialState,
    setGames: (state, action: PayloadAction<GameInfo[]>) => {
      state.games = action.payload
    },

    initApiCall: (state) => {
      state.loading = true
      state.error = null
    },
    finishApiCall: (state) => {
      state.loading = false
    },
    apiCallFailure: (state, action: PayloadAction<string>) => {
      state.loading = false
      state.error = action.payload
    },
  },
})

export const {
  startGame,
  makeMove,
  setGameState,
  setWinner,
  resetGame,
  setGames,
  initApiCall,
  finishApiCall,
  apiCallFailure,
} = gameSlice.actions
export default gameSlice.reducer
