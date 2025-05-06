# model.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class SideStackerNet(nn.Module):
    def __init__(self, board_size=7):
        super().__init__()
        self.conv1 = nn.Conv2d(2, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.policy_head = nn.Linear(64 * board_size * board_size, board_size * 2)
        self.value_head = nn.Linear(64 * board_size * board_size, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        policy = self.policy_head(x)
        value = torch.tanh(self.value_head(x))
        return policy, value
