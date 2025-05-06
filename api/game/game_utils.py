from .constants import BOARD_SIZE
from typing import List, Tuple

def get_valid_moves(board: List[List[int]]) -> List[Tuple[int, str]]:
    valid_moves = []
    for row_index, row in enumerate(board):
        # Left to right
        try:
            left_index = row.index(0)
            valid_moves.append((row_index, 'L'))
        except ValueError:
            pass  # No empty cell from left

        # Right to left
        try:
            right_index = len(row) - 1 - row[::-1].index(0)
            if right_index != left_index:
                valid_moves.append((row_index, 'R'))
        except ValueError:
            pass  # No empty cell from right

    return valid_moves

def apply_move(board: List[List[int]], row: int, direction: str, player: str) -> List[List[int]]:
    board = [list(r) for r in board]
    if direction == 'L':
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                board[row][col] = player
                break
    else:
        for col in reversed(range(BOARD_SIZE)):
            if board[row][col] == 0:
                board[row][col] = player
                break
    return board

def check_winner(board: List[List[int]]):
    def check_line(line: List[int]) -> int:
        for i in range(len(line) - 3):
            window = line[i:i+4]
            if sum(window) == 4:
                return 1
            elif sum(window) == -4:
                return -1
        return 0

    for row in board:
        if (res := check_line(row)) != 0:
            return res
    for col in zip(*board):
        if (res := check_line(col)) != 0:
            return res
    for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
        diag1 = [board[i][i - d] for i in range(max(d, 0), min(BOARD_SIZE + d, BOARD_SIZE)) if 0 <= i - d < BOARD_SIZE]
        diag2 = [board[i][BOARD_SIZE - 1 - i + d] for i in range(max(-d, 0), min(BOARD_SIZE - d, BOARD_SIZE)) if 0 <= BOARD_SIZE - 1 - i + d < BOARD_SIZE]
        if (res := check_line(diag1)) != 0:
            return res
        if (res := check_line(diag2)) != 0:
            return res
    return 0