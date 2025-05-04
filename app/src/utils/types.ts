export interface GameMove {
  row: number
  direction: 'L' | 'R'
  player: number
}

export interface GameInfo {
  id: string
  creator: string
}
