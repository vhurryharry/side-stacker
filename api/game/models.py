from django.db import models
import uuid
import torch
import torch.nn as nn
from .enums import GameStatus, GameMode, BotDifficulty
from .constants import BOARD_SIZE, NUM_ACTIONS


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mode = models.CharField(max_length=10, choices=GameMode.choices, default=GameMode.PVP)
    bot_difficulty = models.CharField(max_length=10, choices=BotDifficulty.choices, null=True, blank=True)
    status = models.CharField(max_length=15, choices=GameStatus.choices, default=GameStatus.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100, null=True, blank=True)
    current_turn = models.IntegerField(default=1)  # 1 for player1, -1 for player2
    
    # Store all moves in the game
    moves = models.ManyToManyField('Move', related_name='games', blank=True)

    def __str__(self):
        return f"Game {self.id} ({self.get_mode_display()})"
    
    def serialize(self):
        return {
            "id": str(self.id),
            "player1": self.player1,
            "player2": self.player2,
            "currentTurn": self.current_turn,
            "mode": self.mode,
            "botDifficulty": self.bot_difficulty,
            "status": self.status,
            "createdAt": self.created_at.isoformat(),
        }
    
    def apply_move(self, row: int, direction: str, current_turn: int):
        if current_turn == 1:
            player_name = getattr(self, "player1", "Player 1")
            player_type = "human" if self.mode != "bvb" else "bot"
        else:
            player_name = getattr(self, "player2", "Player 2")
            player_type = "bot" if self.mode in ["pvb", "bvb"] else "human"

        self.moves.create(
            player_name=player_name,
            player_type=player_type,
            row=row,
            direction=direction
        )

    def get_board(self):
        board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        moves = list(self.moves.all())
        
        for i, move in enumerate(moves):
            symbol = 1 if i % 2 == 0 else -1
            if move.direction == 'L':
                for col in range(BOARD_SIZE):
                    if board[move.row][col] == 0:
                        board[move.row][col] = symbol
                        break
            elif move.direction == 'R':
                for col in reversed(range(BOARD_SIZE)):
                    if board[move.row][col] == 0:
                        board[move.row][col] = symbol
                        break

        return board


class Move(models.Model):
    player_name = models.CharField(max_length=100)
    player_type = models.CharField(max_length=10, choices=[('human', 'Human'), ('bot', 'Bot')], default='human')
    row = models.IntegerField()
    direction = models.CharField(max_length=1, choices=[('L', 'Left'), ('R', 'Right')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Move by {self.player_name} at row {self.row} direction {self.direction}"
