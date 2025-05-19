from django.test import TestCase
from game.models import Game, Move
from game.enums import GameMode, GameStatus
import pytest
import pytest_asyncio

class GameModelTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create(
            player1="Alice",
            player2="Bob",
            mode=GameMode.PVP,
            status=GameStatus.WAITING
        )

    def test_game_creation(self):
        self.assertEqual(self.game.player1, "Alice")
        self.assertEqual(self.game.player2, "Bob")
        self.assertEqual(self.game.mode, GameMode.PVP)
        self.assertEqual(self.game.status, GameStatus.WAITING)

    def test_game_str(self):
        self.assertIn(str(self.game.id), str(self.game))

    def test_serialize(self):
        data = self.game.serialize()
        self.assertEqual(data["player1"], "Alice")
        self.assertEqual(data["player2"], "Bob")
        self.assertEqual(data["mode"], GameMode.PVP)
        self.assertEqual(data["status"], GameStatus.WAITING)

@pytest.mark.django_db(transaction=True)
class TestGameModelAsync:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_game(self, db):
        from game.models import Game
        from game.enums import GameMode, GameStatus
        from asgiref.sync import sync_to_async
        self.game = await sync_to_async(Game.objects.create)(
            player1="Alice",
            player2="Bob",
            mode=GameMode.PVP,
            status=GameStatus.WAITING
        )

    async def test_get_board_empty(self):
        from game.constants import BOARD_SIZE
        board = await self.game.get_board()
        assert len(board) == BOARD_SIZE
        assert all(len(row) == BOARD_SIZE for row in board)
        assert all(cell == 0 for row in board for cell in row)

    async def test_apply_move_and_get_board(self):
        board, winner, is_draw = await self.game.apply_move(0, 'L', 1)
        assert board[0][0] == 1
        assert winner is 0
        assert not is_draw
        board, winner, is_draw = await self.game.apply_move(0, 'R', -1)
        assert board[0][-1] == -1
        assert winner is 0
        assert not is_draw

class MoveModelTestCase(TestCase):
    def setUp(self):
        self.move = Move.objects.create(
            player_name="Alice",
            player_type="human",
            row=0,
            direction="L"
        )

    def test_move_creation(self):
        self.assertEqual(self.move.player_name, "Alice")
        self.assertEqual(self.move.player_type, "human")
        self.assertEqual(self.move.row, 0)
        self.assertEqual(self.move.direction, "L")

    def test_move_str(self):
        self.assertIn("Move by Alice", str(self.move))
