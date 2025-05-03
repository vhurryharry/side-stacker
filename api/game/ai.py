import random
import torch
import numpy as np
from .models import SideStackerModel

# Constants
BOARD_SIZE = 7
NUM_ACTIONS = BOARD_SIZE * 2

# --- AI Model ---
class SideStackerModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(BOARD_SIZE * BOARD_SIZE, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, NUM_ACTIONS)

    def forward(self, x):
        x = x.view(-1, BOARD_SIZE * BOARD_SIZE)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# --- AI Functions ---
def encode_board(board):
    return torch.tensor(board, dtype=torch.float32).unsqueeze(0)

def get_valid_moves(board):
    valid_moves = []
    for row in range(BOARD_SIZE):
        if board[row][0] == 0:
            valid_moves.append((row, 'L'))
        if board[row][-1] == 0:
            valid_moves.append((row, 'R'))
    return valid_moves

def apply_move(board, row, direction, player):
    board = [list(r) for r in board]
    if direction == 'L':
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                board[row][col] = player
                break
    else:
        for col in reversed(range(BOARD_SIZE)):
            if board[row][col] == 0:
                board[row][col] = player
                break
    return board

def check_winner(board):
    def check_line(line):
        for i in range(len(line) - 3):
            window = line[i:i+4]
            if sum(window) == 4:
                return 1
            elif sum(window) == -4:
                return -1
        return 0

    for row in board:
        if (res := check_line(row)) != 0:
            return res
    for col in zip(*board):
        if (res := check_line(col)) != 0:
            return res
    for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
        diag1 = [board[i][i - d] for i in range(max(d, 0), min(BOARD_SIZE + d, BOARD_SIZE)) if 0 <= i - d < BOARD_SIZE]
        diag2 = [board[i][BOARD_SIZE - 1 - i + d] for i in range(max(-d, 0), min(BOARD_SIZE - d, BOARD_SIZE)) if 0 <= BOARD_SIZE - 1 - i + d < BOARD_SIZE]
        if (res := check_line(diag1)) != 0:
            return res
        if (res := check_line(diag2)) != 0:
            return res
    return 0

def get_q_target(q_values, action_idx, reward, next_q_values, done):
    return reward if done else reward + 0.9 * torch.max(next_q_values).item()

def train_bvb(model, episodes=1000):
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
