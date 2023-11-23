from torch import nn
import torch
from torch.nn import functional as F

from wml_ai_model_managers.vision_model_manager_zero.feedforward import FeedFoward
from wml_ai_model_managers.vision_model_manager_zero.multi_head_attention import MultiHeadAttention



class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, n_embd, n_head,dropout,block_size):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size,dropout,n_embd,block_size)
        self.ffwd = FeedFoward(n_embd,dropout)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        y = self.sa(x)
        x = self.ln1(x + y)
        y = self.ffwd(x)
        x = self.ln2(x + y)
        return x

