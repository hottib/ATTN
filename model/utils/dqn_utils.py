from collections import namedtuple, deque
import random

# A named tuple representing a single transition in our environment. 
# It essentially maps (state, action) pairs to their (next_state, reward) result
Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))
class ReplayMemory(object):
'''
A cyclic buffer of bounded size that holds the transitions observed recently. 
It also implements a .sample() method for selecting a random batch of transitions for training.
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
'''
    def __init__(self, capacity):
        '''
        params: capacity - size of memory
        '''
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)