import torch
import numpy as np
from .model import SideStackerNet
from ..game_utils import get_valid_moves, check_winner, apply_move
from ..constants import BOARD_SIZE

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "./game/ai/hard_model.pth"

# Load model once
model = SideStackerNet().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

def board_to_tensor(board, player):
    p1 = [[1 if cell == player else 0 for cell in row] for row in board]
    p2 = [[1 if cell == -player else 0 for cell in row] for row in board]
    tensor = torch.tensor([p1, p2], dtype=torch.float32).unsqueeze(0)
    return tensor.to(device)


def is_safe_move(board, move, player, depth=2):
    opponent = -player
    test_board = apply_move(board, move[0], move[1], player)

    def opponent_can_win(b, p):
        if check_winner(b) == p:
            return True
        for mv in get_valid_moves(b):
            b2 = apply_move(b, mv[0], mv[1], p)
            if check_winner(b2) == p:
                return True
        return False

    queue = [(test_board, 0)]
    while queue:
        current_board, d = queue.pop(0)
        if d >= depth:
            continue
        if opponent_can_win(current_board, opponent):
            return False
        for mv in get_valid_moves(current_board):
            next_board = apply_move(current_board, mv[0], mv[1], opponent)
            queue.append((next_board, d + 1))

    return True

# ✅ Use trained model to choose the best safe move
def predict_move(board, player):
    tensor_input = board_to_tensor(board, player)
    with torch.no_grad():
        policy_logits, _ = model(tensor_input)
        policy = torch.softmax(policy_logits, dim=1).cpu().numpy()[0]

    valid_moves = get_valid_moves(board)
    safe_moves = [mv for mv in valid_moves if is_safe_move(board, mv, player)]

    if not safe_moves:
        safe_moves = valid_moves  # fallback if no safe moves found

    move_indices = {(r, d): i for i, (r, d) in enumerate([(r, s) for r in range(BOARD_SIZE) for s in ['L', 'R']])}
    scored_moves = [(mv, policy[move_indices[mv]]) for mv in safe_moves]

    best_move = max(scored_moves, key=lambda x: x[1])[0]
    return best_move
