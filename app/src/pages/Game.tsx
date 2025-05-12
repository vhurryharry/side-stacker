import React, { useEffect, useRef, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '../store'
import { useNavigate } from 'react-router-dom'
import {
  connectWebSocket,
  disconnectWebSocket,
  isSocketConnected,
  sendMessage,
  subscribeToMessages,
} from '../utils/socket'
import GameBoard from '../components/GameBoard'
import { GameMode, GameStatus } from '../utils/enums'
import LoadingSpinner from '../components/LoadingSpinner'
import { joinGame, setWinner, makeMove, setDraw, resetGame } from '../reducers/gameSlice'
import { isValidMove } from '../utils/utils'

const Game: React.FC = () => {
  const navigate = useNavigate()
  const {
    id,
    player1,
    player2,
    currentTurn,
    myTurn,
    winner,
    mode,
    botDifficulty,
    status,
    board,
    isDraw,
  } = useSelector((state: RootState) => state.game)
  const dispatch = useDispatch<AppDispatch>()
  const [aiTrigger, setAiTrigger] = useState<number>()
  // Double useEffect guard in React dev mode
  const ranOnce = useRef(false)

  const wsHandler = (data: any) => {
    console.log('websocket received', data)

    if (data.type === 'player_join') {
      dispatch(
        joinGame({
          player2: data.player2,
        })
      )
    } else if (data.type === 'move') {
      const { row, direction, winner, isDraw, currentTurn: turn } = data
      dispatch(
        makeMove({
          row,
          direction,
          turn,
        })
      )

      if (winner || isDraw) {
        clearInterval(aiTrigger)
      }

      if (winner) {
        dispatch(setWinner(winner))
      }
      if (isDraw) {
        dispatch(setDraw())
      }
    }
  }

  const triggerAIMove = () => {
    sendMessage({
      id,
      message: {
        turn: myTurn,
      },
    })
  }

  useEffect(() => {
    if (!ranOnce.current) {
      ranOnce.current = true

      if (id) {
        if (!isSocketConnected()) {
          connectWebSocket(id)

          subscribeToMessages(wsHandler)

          if (mode === GameMode.BVB && !aiTrigger) {
            setAiTrigger(setInterval(triggerAIMove, 1000))
          }
        }
      } else {
        navigate('/')
      }
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const onCellClick = (row: number, col: number) => {
    const { valid, direction } = isValidMove(row, col, board)
    if (valid && direction) {
      sendMessage({
        id,
        message: {
          row,
          direction,
          turn: myTurn,
        },
      })
    }
  }

  const closeGame = () => {
    disconnectWebSocket()
    dispatch(resetGame())
    clearInterval(aiTrigger)
    navigate('/')
  }

  return (
    <div className="w-full flex flex-col items-center h-screen">
      <span className="text-xl">
        {mode === GameMode.PVP
          ? 'Player vs Player'
          : mode === GameMode.PVB
            ? 'Player vs Bot'
            : 'Bot vs Bot'}
        {mode === GameMode.PVB && ` (${botDifficulty})`}
      </span>

      <div className="flex flex-row items-center justify-around w-1/2 mt-4">
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
          {winner &&
            `${winner === 1 ? 'Player 1 (' + player1 + ')' : 'Player 2 (' + player2 + ')'} won!`}
        </div>
      )}
      {isDraw && <div className="mt-4 text-2xl font-bold">It's a draw!</div>}
      <GameBoard
        board={board}
        currentTurn={currentTurn}
        onCellClick={onCellClick}
        myTurn={myTurn}
        disabled={status !== GameStatus.IN_PROGRESS || myTurn !== currentTurn}
      />
      {status === GameStatus.FINISHED && (
        <button onClick={closeGame} className="btn mt-8">
          Back to Main Menu
        </button>
      )}
    </div>
  )
}

export default Game
