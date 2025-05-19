import pytest
from channels.testing import WebsocketCommunicator
from backend.asgi import application
from game.models import Game
from game.enums import GameMode, GameStatus
import json
from asgiref.sync import sync_to_async
import uuid

pytestmark = pytest.mark.django_db(transaction=True)

@pytest.mark.asyncio
class TestGameConsumer:
    async def test_connect_and_disconnect(self):
        game = await sync_to_async(Game.objects.create)(player1="Alice", mode=GameMode.PVP, status=GameStatus.WAITING)
        communicator = WebsocketCommunicator(application, f"/ws/game/{game.id}/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_receive_invalid_game_id(self):
        # Use a valid UUID that does not exist in the database
        game = await sync_to_async(Game.objects.create)(player1="Alice", mode=GameMode.PVP, status=GameStatus.WAITING)
        communicator = WebsocketCommunicator(application, f"/ws/game/{game.id}/")
        await communicator.connect()
        non_existent_id = str(uuid.uuid4())
        await communicator.send_to(text_data=json.dumps({"id": non_existent_id, "message": {}}))
        response = await communicator.receive_from()
        data = json.loads(response)
        assert "error" in data
        await communicator.disconnect()

    async def test_game_play_valid_moves(self):
        game = await sync_to_async(Game.objects.create)(player1="Alice", player2="Bob", mode=GameMode.PVP, status=GameStatus.IN_PROGRESS, current_turn=1)
        communicator = WebsocketCommunicator(application, f"/ws/game/{game.id}/")
        connected, _ = await communicator.connect()
        assert connected

        # Player 1 makes a valid move
        await communicator.send_to(text_data=json.dumps({
            "id": str(game.id),
            "message": {"turn": 1, "row": 0, "direction": "L"}
        }))
        response = await communicator.receive_from()
        data = json.loads(response)
        assert data["type"] == "move"
        assert data["row"] == 0
        assert data["direction"] == "L"
        assert data["currentTurn"] == 1
        assert data["winner"] is None
        assert data["isDraw"] is False

        # Player 2 makes a valid move
        await communicator.send_to(text_data=json.dumps({
            "id": str(game.id),
            "message": {"turn": -1, "row": 0, "direction": "R"}
        }))
        response = await communicator.receive_from()
        data = json.loads(response)
        assert data["type"] == "move"
        assert data["row"] == 0
        assert data["direction"] == "R"
        assert data["currentTurn"] == -1
        assert data["winner"] is None
        assert data["isDraw"] is False

        await communicator.disconnect()

    async def test_game_play_invalid_move(self):
        game = await sync_to_async(Game.objects.create)(player1="Alice", player2="Bob", mode=GameMode.PVP, status=GameStatus.IN_PROGRESS, current_turn=1)
        communicator = WebsocketCommunicator(application, f"/ws/game/{game.id}/")
        connected, _ = await communicator.connect()
        assert connected

        # Player 1 makes a valid move
        await communicator.send_to(text_data=json.dumps({
            "id": str(game.id),
            "message": {"turn": 1, "row": 0, "direction": "L"}
        }))
        await communicator.receive_from()

        # Player 1 tries to move again (not their turn)
        await communicator.send_to(text_data=json.dumps({
            "id": str(game.id),
            "message": {"turn": 1, "row": 1, "direction": "L"}
        }))
        response = await communicator.receive_from()
        data = json.loads(response)
        assert "error" in data
        assert data["error"] == "Not your turn!"

        await communicator.disconnect()
