import torch
import random
from .models import SideStackerModel
from .game_utils import get_valid_moves, apply_move, check_winner
from .ai import encode_board

def load_model(model_path="models/hard_ai.pth") -> SideStackerModel:
    model = SideStackerModel()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def get_easy_ai_move(board: list[list[int]], player: int) -> tuple[int, str]:
    valid_moves = get_valid_moves(board)
    return random.choice(valid_moves)

def get_medium_ai_move(board: list[list[int]], player: int) -> tuple[int, str]:
    valid_moves = get_valid_moves(board)

    for move in valid_moves:
        new_board = apply_move(board, *move, player)
        if check_winner(new_board) == player:
            return move

    for move in valid_moves:
        new_board = apply_move(board, *move, -player)
        if check_winner(new_board) == -player:
            return move

    return random.choice(valid_moves)

def get_hard_ai_move(board: list[list[int]], player: int) -> tuple[int, str]:
    model = load_model()
    valid_moves = get_valid_moves(board)
    state_tensor = encode_board(board)
    q_values = model(state_tensor).detach().numpy().squeeze()

    move_scores = {}
    for row, direction in valid_moves:
        idx = row * 2 + (0 if direction == 'L' else 1)
        move_scores[(row, direction)] = q_values[idx]

    best_move = max(move_scores, key=move_scores.get)
    return best_move

def get_ai_move(board: list[list[int]], difficulty: str, player: int) -> tuple[int, str]:
    if difficulty == 'easy':
        return get_easy_ai_move(board, player)
    elif difficulty == 'medium':
        return get_medium_ai_move(board, player)
    elif difficulty == 'hard':
        return get_hard_ai_move(board, player)
    else:
        raise ValueError(f"Unknown difficulty level: {difficulty}")
