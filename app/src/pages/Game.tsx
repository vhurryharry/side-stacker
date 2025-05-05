import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '../store'
import { useNavigate } from 'react-router-dom'

const Game: React.FC = () => {
  const navigate = useNavigate()
  const { loading, error, id } = useSelector((state: RootState) => state.game)

  useEffect(() => {}, [])

  return (
    <div className="game-container">
      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}
      {!loading && !error && <div className="game-id">Game ID: {id}</div>}
      {/* Add game board and controls here */}
      <h1>Side Stacker</h1>
      <div className="game-board">{/* Game board implementation goes here */}</div>
      <div className="controls">{/* Game controls (e.g., buttons) go here */}</div>
    </div>
  )
}

export default Game
