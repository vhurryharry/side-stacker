import torch
import numpy as np
from .model import SideStackerNet
from ..game_utils import get_valid_moves
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

def predict_move(board, player):
    valid_moves = get_valid_moves(board)
    state_tensor = board_to_tensor(board, player)
    with torch.no_grad():
        policy_logits, _ = model(state_tensor)
        policy_probs = torch.softmax(policy_logits, dim=1).cpu().numpy()[0]  # shape: [14]
    
    move_map = [(row, dir) for row in range(BOARD_SIZE) for dir in ['L', 'R']]
    legal_probs = []
    legal_moves = []

    for i, move in enumerate(move_map):
        if move in valid_moves:
            legal_moves.append(move)
            legal_probs.append(policy_probs[i])
    
    if not legal_moves:
        return None

    # Normalize probabilities among valid moves
    total = sum(legal_probs)
    norm_probs = [p / total for p in legal_probs]
    chosen_index = np.argmax(norm_probs)  # or use random.choices(...) for exploration

    return legal_moves[chosen_index]
