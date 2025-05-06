import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '../store'
import { useNavigate } from 'react-router-dom'
import {
  connectWebSocket,
  disconnectWebSocket,
  isSocketConnected,
  subscribeToMessages,
} from '../utils/socket'
import GameBoard from '../components/GameBoard'
import { makeMove } from '../middlewares/gameMiddleware'
import { GameMode, GameStatus } from '../utils/enums'
import LoadingSpinner from '../components/LoadingSpinner'
import { joinGame, setWinner, makeMove as reduxMakeMove } from '../reducers/gameSlice'
import { isValidMove } from '../utils/utils'

const Game: React.FC = () => {
  const navigate = useNavigate()
  const {
    id,
    loading,
    error,
    player1,
    player2,
    currentTurn,
    myTurn,
    winner,
    mode,
    botDifficulty,
    status,
    board,
  } = useSelector((state: RootState) => state.game)
  const dispatch = useDispatch<AppDispatch>()

  const wsHandler = (data: any) => {
    console.log('websocket received', data)
    if (data.type === 'player_join') {
      dispatch(
        joinGame({
          player2: data.player2,
        })
      )
    } else if (data.type === 'move') {
      const { row, side, winner } = data
      dispatch(
        reduxMakeMove({
          row,
          direction: side,
        })
      )

      if (winner) {
        dispatch(setWinner(winner))
      }
    }
  }

  useEffect(() => {
    if (id) {
      if (!isSocketConnected()) {
        connectWebSocket(id)

        subscribeToMessages(wsHandler)
      }
    } else {
      navigate('/')
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const onCellClick = (row: number, col: number) => {
    const { valid, direction } = isValidMove(row, col, board)
    if (valid && direction) {
      dispatch(makeMove(id, row, direction))
    }
  }

  return (
    <div className="w-full flex flex-col items-center h-screen">
      <span className="text-xl">
        {mode === GameMode.PVP
          ? 'Player vs Player'
          : mode === GameMode.PVB
            ? 'Player vs Bot'
            : 'Bot vs Bot'}
      </span>

      <div className="flex flex-row items-center justify-around w-1/2">
        <span className={`text-xl ${currentTurn === 1 && 'font-bold'}`}>Player 1: {player1}</span>
        <span className={`text-xl ${currentTurn === -1 && 'font-bold'}`}>Player 2: {player2}</span>
      </div>

      {status === GameStatus.WAITING && (
        <div className="mt-4">
          <div className="text-lg mb-4">Waiting for another player...</div>
          <LoadingSpinner />
        </div>
      )}
      {winner && (
        <div className="mt-4 text-2xl font-bold">
          {winner && `Winner: ${winner === 1 ? player1 : player2}`}
        </div>
      )}
      <GameBoard
        board={board}
        currentTurn={currentTurn}
        onCellClick={onCellClick}
        myTurn={myTurn}
        disabled={status !== GameStatus.IN_PROGRESS || winner !== null || myTurn !== currentTurn}
      />
      <div className="controls">{/* Game controls (e.g., buttons) go here */}</div>
    </div>
  )
}

export default Game
