import random
from .ai.ai_inference import predict_move
from .game_utils import get_valid_moves, apply_move, check_winner

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
    return predict_move(board, player)

def get_ai_move(board: list[list[int]], difficulty: str, player: int) -> tuple[int, str]:
    if difficulty == 'easy':
        return get_easy_ai_move(board, player)
    elif difficulty == 'medium':
        return get_medium_ai_move(board, player)
    elif difficulty == 'hard':
        return get_hard_ai_move(board, player)
    else:
        raise ValueError(f"Unknown difficulty level: {difficulty}")
