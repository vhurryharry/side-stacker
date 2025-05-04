import React from 'react'

const Game: React.FC = () => {
  return (
    <div className="game-container">
      <h1>Side Stacker</h1>
      <div className="game-board">{/* Game board implementation goes here */}</div>
      <div className="controls">{/* Game controls (e.g., buttons) go here */}</div>
    </div>
  )
}

export default Game
