# Placeholder for future utility tests
from django.test import TestCase
from game.game_utils import get_valid_moves, apply_move, check_winner
from game.constants import BOARD_SIZE

class GameUtilsTestCase(TestCase):
    def setUp(self):
        self.empty_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def test_get_valid_moves_empty(self):
        moves = get_valid_moves(self.empty_board)
        self.assertEqual(len(moves), BOARD_SIZE * 2)

    def test_apply_move_left_and_right(self):
        board = apply_move(self.empty_board, 0, 'L', 1)
        self.assertEqual(board[0][0], 1)
        board = apply_move(board, 0, 'R', -1)
        self.assertEqual(board[0][-1], -1)

    def test_check_winner_none(self):
        self.assertEqual(check_winner(self.empty_board), 0)

    def test_check_winner_row(self):
        board = [row[:] for row in self.empty_board]
        for i in range(4):
            board[0][i] = 1
        self.assertEqual(check_winner(board), 1)

    def test_check_winner_col(self):
        board = [row[:] for row in self.empty_board]
        for i in range(4):
            board[i][0] = -1
        self.assertEqual(check_winner(board), -1)

    def test_check_winner_diag(self):
        board = [row[:] for row in self.empty_board]
        for i in range(4):
            board[i][i] = 1
        self.assertEqual(check_winner(board), 1)
