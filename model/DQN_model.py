import gymnasium as gym
import math
"""
27.03.23
This is our first model following the assumption that DQN model 
(from this articel https://towardsdatascience.com/reinforcement-learning-101-e24b50e1d292)
will serve our purpose.
The code is taken from https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
"""

import torch
import torch.nn as nn

class DQN(nn.Module):
'''
Small DQN model
params: n_observations - number of input observations
        n_actions - number of output actions
'''
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)