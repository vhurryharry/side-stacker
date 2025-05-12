from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from .ai_move import get_ai_move
from .enums import GameMode, GameStatus
from .game_utils import get_valid_moves

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.group_name = f"game_{self.game_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        def error_response(message):
            return self.send(text_data=json.dumps({'error': message}))
        
        data = json.loads(text_data)
        message = data.get('message')
        game_id = data.get('id')

        if not game_id:
            return await error_response('Game ID is required!')
        
        from .models import Game
        try:
            game = await database_sync_to_async(Game.objects.get)(id=game_id)
        except Game.DoesNotExist:
            return await error_response('Game not found!')

        # Handle Player Move
        if game.mode in [GameMode.PVP, GameMode.PVB]:
            if game.current_turn != int(message.get('turn')):
                return await error_response('Not your turn!')
            
            row = int(message.get('row'))
            direction = message.get('direction')
            board = await game.get_board()

            # Validate move
            if (row, direction) not in get_valid_moves(board):
                return await error_response('Invalid move')

            board, winner, is_draw = await game.apply_move(row, direction, game.current_turn)
            await self.send_game_update(game_id, row, direction, board, game.current_turn, winner, is_draw)

        # Handle AI Move
        if game.status != GameStatus.FINISHED and game.mode in [GameMode.PVB, GameMode.BVB]:
            board = await game.get_board()
            ai_move = get_ai_move(board, game.bot_difficulty, game.current_turn)
            row, direction = ai_move
            board, winner, is_draw = await game.apply_move(row, direction, game.current_turn)
            await self.send_game_update(game_id, row, direction, board, game.current_turn, winner, is_draw)

    async def send_game_update(self, game_id, row, direction, board, current_turn, winner, is_draw):
        await self.channel_layer.group_send(
            f"game_{game_id}",
            {
                "type": "game_update",
                "message": {
                    "type": "move",
                    "row": row,
                    "direction": direction,
                    "board": board,
                    "currentTurn": -current_turn,   # Current turn is switched after move
                    "winner": winner if winner else None,
                    "isDraw": is_draw,
                },
            },
        )

    async def game_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))
