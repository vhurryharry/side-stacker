import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.game_id = self.scope['url_route']['kwargs']['game_id']  # Get game_id from URL
        self.room_group_name = f"game_{self.game_id}"  # You can use this to route messages to specific games

        # Join the game room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send a message to WebSocket
        await self.send(text_data=json.dumps({
            'message': 'Welcome to the game!'
        }))

    async def disconnect(self, close_code):
        # Leave the game room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from WebSocket
        data = json.loads(text_data)

        # Handle received message (e.g., handle game moves)
        move = data.get('move', None)

        # Send the move to all WebSocket clients in the game room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_move',
                'move': move
            }
        )

    async def game_move(self, event):
        # Send the move to WebSocket
        await self.send(text_data=json.dumps({
            'move': event['move']
        }))
