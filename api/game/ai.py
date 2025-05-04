import random
import torch
from .models import SideStackerModel
from .game_utils import get_valid_moves, apply_move, check_winner
from .constants import BOARD_SIZE, NUM_ACTIONS

def encode_board(board):
    return torch.tensor(board, dtype=torch.float32).unsqueeze(0)

def get_q_target(q_values, action_idx, reward, next_q_values, done):
    return reward if done else reward + 0.9 * torch.max(next_q_values).item()

def train_bvb(model: SideStackerModel, episodes=1000):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.MSELoss()

    for ep in range(episodes):
        board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        player = 1
        for turn in range(BOARD_SIZE**2):
            state_tensor = encode_board(board)
            q_values = model(state_tensor)
            q_np = q_values.detach().numpy().squeeze()

            valid_moves = get_valid_moves(board)
            if not valid_moves:
                break

            # Select action based on epsilon-greedy strategy
            if random.random() < 0.1:  # Exploration
                move = random.choice(valid_moves)
            else:  # Exploitation
                indices = [(r * 2 + (0 if d == 'L' else 1)) for r, d in valid_moves]
                best_idx = max(indices, key=lambda idx: q_np[idx])
                move = (best_idx // 2, 'L' if best_idx % 2 == 0 else 'R')

            move_idx = move[0] * 2 + (0 if move[1] == 'L' else 1)
            next_board = apply_move(board, *move, player)
            winner = check_winner(next_board)

            reward = 1 if winner == player else -1 if winner == -player else 0
            done = winner != 0

            next_tensor = encode_board(next_board)
            with torch.no_grad():
                next_q = model(next_tensor)

            target = q_values.clone()
            target[0][move_idx] = get_q_target(q_values, move_idx, reward, next_q, done)

            optimizer.zero_grad()
            loss = loss_fn(q_values, target)
            loss.backward()
            optimizer.step()

            board = next_board
            player *= -1
            if done:
                break

        if ep % 100 == 0:
            print(f"Episode {ep}, loss: {loss.item():.4f}")
