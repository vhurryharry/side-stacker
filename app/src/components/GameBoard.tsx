import React from 'react'

interface IProps {
  board: number[][]
  onCellClick: (row: number, col: number) => void
  currentTurn: number
  myTurn: number
  disabled?: boolean
}

const GameBoard: React.FC<IProps> = ({
  board,
  onCellClick,
  currentTurn,
  myTurn,
  disabled,
}: IProps) => {
  return (
    <div
      className={`grid grid-cols-7 gap-1 mt-8 ${disabled ? 'pointer-events-none opacity-50' : ''}`}
      style={{ gridTemplateColumns: `repeat(${board[0].length}, 3rem)` }}
    >
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => {
          const value = cell === 1 ? 'X' : cell === -1 ? 'O' : ''
          return (
            <div
              key={`${rowIndex}-${colIndex}`}
              onClick={() => onCellClick?.(rowIndex, colIndex)}
              className={`
                w-12 h-12 border border-gray-500 flex items-center justify-center
                text-xl font-bold cursor-pointer transition
                ${value === '' && myTurn === currentTurn ? 'hover:bg-gray-700' : 'cursor-default'}
              `}
            >
              {value}
            </div>
          )
        })
      )}
    </div>
  )
}

export default GameBoard
