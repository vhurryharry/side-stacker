import torch
import torch.nn as nn

BOARD_SIZE = 7
NUM_ACTIONS = BOARD_SIZE * 2  # 7 rows x 2 sides (L/R)

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
