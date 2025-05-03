import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { BotDifficulty, GameMode, GameStatus } from '../utils/enums'
import { GameMove } from '../utils/types'

interface GameState {
  gameId: string
  currentGameStatus: GameStatus
  moveHistory: GameMove[]
  gameMode: GameMode
  botDifficulty: BotDifficulty
  board: number[][]
  currentTurn: number
  winner: number | null
}

const initialState: GameState = {
  gameId: '',
  currentGameStatus: GameStatus.WAITING,
  moveHistory: [],
  gameMode: GameMode.PVP,
  botDifficulty: BotDifficulty.MEDIUM,
  board: Array(7).fill(Array(7).fill(0)),
  currentTurn: 1, // Player 1 starts
  winner: null,
}

const gameSlice = createSlice({
  name: 'game',
  initialState,
  reducers: {
    startGame: (
      state,
      action: PayloadAction<{
        gameId: string
        gameMode: GameMode
        botDifficulty?: BotDifficulty
      }>
    ) => {
      state.gameId = action.payload.gameId
      state.currentGameStatus = GameStatus.IN_PROGRESS
      state.gameMode = action.payload.gameMode
      if (action.payload.gameMode === GameMode.PVB) {
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
        gameId: string
        board: number[][]
        currentTurn: number
        currentGameStatus: GameStatus
        moveHistory: GameMove[]
      }>
    ) => {
      state.gameId = action.payload.gameId
      state.board = action.payload.board
      state.currentTurn = action.payload.currentTurn
      state.currentGameStatus = action.payload.currentGameStatus
      state.moveHistory = action.payload.moveHistory
    },
    setWinner: (state, action: PayloadAction<number>) => {
      state.winner = action.payload
      state.currentGameStatus = GameStatus.COMPLETED
    },
    resetGame: () => initialState,
  },
})

export const { startGame, makeMove, setGameState, setWinner, resetGame } = gameSlice.actions
export default gameSlice.reducer
