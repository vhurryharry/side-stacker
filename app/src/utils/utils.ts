type Direction = 'L' | 'R'

interface ValidMoveResult {
  valid: boolean
  direction?: Direction
}

export function isValidMove(row: number, col: number, board: number[][]): ValidMoveResult {
  const rowData = board[row]

  // Find first empty from left
  const leftIndex = rowData.findIndex((cell) => cell === 0)
  if (leftIndex === col) {
    return { valid: true, direction: 'L' }
  }

  // Find first empty from right
  const rightIndex = rowData.length - 1 - [...rowData].reverse().findIndex((cell) => cell === 0)
  if (rightIndex === col) {
    return { valid: true, direction: 'R' }
  }

  return { valid: false }
}
