import os
import time
import requests
import torch
import torch.nn as nn
from torch.nn import functional as F
import mmap
import random
import pickle
import argparse
from tqdm import tqdm

from wml_ai_model_managers.text_model_manager_one.dataset import WMLDataset
from wml_ai_model_managers.text_model_manager_one.model import WMLTextOneModel
from wml_ai_model_managers.text_model_manager_one.block import WMLTextOneBlock
from wml_ai_model_managers.text_model_manager_one.feedforward import WMLTextOneFeedFoward
from wml_ai_model_managers.text_model_manager_one.multi_head_attention import WMLTextOneMultiHead
from wml_ai_model_managers.text_model_manager_one.head import WMLTextOneHead
from wml_ai_model_managers.wml_utils.error_utils import _LogicError
from wml_ai_model_managers.wml_utils.common_utils import xor
from torch.utils.data import DataLoader,Subset
from torchtext.data import datasets_utils

from torchtext import datasets
from wml_ai_model_managers.wml_utils.common_utils import get_device


class WMLTextModelManagerOne():
  def __init__(self,**kwargs) -> None:
    self.block_size =  kwargs.get("block_size",128)
    self.batch_size = kwargs.get("batch_size",64)
    self.device =  kwargs.get("device",get_device())
    self.max_iters = kwargs.get("max_iters",15000)
    self.n_embd = kwargs.get("n_embd", 384)
    self.n_head = kwargs.get("n_head", 4)
    self.n_layer = kwargs.get("n_layer", 8)
    self.dropout = kwargs.get("dropout", 0.1)
    self.reporting_loss = kwargs.get("reporting_loss", 100)
    self.learning_rate = kwargs.get("learning_rate", 3e-4)
    self.model_file_name = kwargs.get("model_file_name",'model-02.pkl')
    self.training_dataloader = kwargs.get("training_dataloader",None)
    self.test_dataloader = kwargs.get("test_dataloader",None)
    self.dataloader_info = kwargs.get("dataloader_info",None)


  def chat_with_model(self,completion_size=150):
    while True:
        prompt = input("Prompt:\n")
        context = torch.tensor(self.encode(prompt), dtype=torch.long, device=self.device)
        generated_chars = self.decode(self.m.generate(context.unsqueeze(0), max_new_tokens=completion_size)[0].tolist())
        print(f'Completion:\n{generated_chars}')

  def load_model_from_scratch(self):
    self.model = WMLTextOneModel(
      vocab_size=self.vocab_size,
      block_size=self.block_size,
      n_embd=self.n_embd,
      n_layer=self.n_layer,
      device=self.device,
      n_head=self.n_head,
      dropout=self.dropout
    )
    self.m = self.model.to(self.device)

  def load_model_from_pickle_file(self):
    with open(self.model_file_name, 'rb') as f:
        self.model = pickle.load(f)
    print('loaded successfully!')
    self.m = self.model.to(self.device)

  def save_model_to_pickle_file(self):
    with open(self.model_file_name,'wb') as f:
      pickle.dump(self.model,f)

  def download_train_and_test_data(self):
      if xor(self.training_dataloader,self.test_dataloader):
        raise _LogicError("if you provide training_dataloader or test_dataloader you must provide the other or else you be testining your training data with a different dataset! If you dont know this is bad!")

      my_root = "data"

      if self.dataloader_info != None:
        training_dataloader_info = self.dataloader_info
        training_dataloader_info["split"] = "train"




        self.training_dataloader = WMLDataset(
          dataloader_info = training_dataloader_info,
        )

        test_dataloader_info = self.dataloader_info
        test_dataloader_info["split"] = "test"

        self.test_dataloader = WMLDataset(
          dataloader_info = test_dataloader_info,
        )

      else:
        if  self.training_dataloader == None:
          self.training_dataloader = WMLDataset(
            datasets.AG_NEWS(
              root=my_root,
              split="train",
            )
          )


        if  self.test_dataloader == None:
          self.test_dataloader = WMLDataset(
            datasets.AG_NEWS(
              root=my_root,
              split="test",
            )
          )

      self._get_vocab_info()
      self._get_encoders()



  def _get_vocab_info(self):

    self.chars = sorted(set( self.training_dataloader.chars + self.test_dataloader.chars))
    self.vocab_size = len(self.chars)

  def _get_encoders(self):
    string_to_int = { ch:i for i,ch in enumerate(self.chars) }
    int_to_string = { i:ch for i,ch in enumerate(self.chars) }
    self.encode = lambda s: [string_to_int[c] for c in s]
    self.decode = lambda l: ''.join([int_to_string[i] for i in l])

  def _get_random_chunk(self,split):
      my_dataset = self.training_dataloader if split == 'train' else self.test_dataloader
      chunk_size = self.block_size*self.batch_size
      random_chunk = my_dataset.get_random_chunk(chunk_size)


      return torch.tensor(self.encode(random_chunk), dtype=torch.long)

  def _get_batch(self,split):
      data = self._get_random_chunk(split)
      ix = torch.randint(len(data) - self.block_size, (self.batch_size,))
      x = torch.stack([data[i:i+self.block_size] for i in ix])
      y = torch.stack([data[i+1:i+self.block_size+1] for i in ix])
      x, y = x.to(self.device), y.to(self.device)
      return x, y

  def train(self):
    print("Starting Training Session")
    context = torch.zeros((1,1), dtype=torch.long, device=self.device)
    generated_chars = self.decode(self.m.generate(context, max_new_tokens=self.vocab_size)[0].tolist())
    self._estimate_loss()
    self._create_optimizer()

  @torch.no_grad()
  def _estimate_loss(self):
      out = {}
      self.model.eval()
      for split in ['train', 'val']:
          losses = torch.zeros(self.reporting_loss)
          for k in range(self.reporting_loss):
              X, Y = self._get_batch(split)
              logits, loss = self.model(X, Y)
              losses[k] = loss.item()
          out[split] = losses.mean()
      self.model.train()
      return out

  def _create_optimizer(self):
    # create a PyTorch optimizer
    optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate)

    start_time = time.time()
    end_time = time.time()
    for iter in tqdm(range(self.max_iters),total=self.max_iters):
        self.iters_left = self.max_iters - iter
        if iter % self.reporting_loss == 0:
            losses = self._estimate_loss()
            end_time = time.time()
            elapsed_time_seconds = end_time - start_time
            hours, remainder = divmod(elapsed_time_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"step: {iter}, train loss: {losses['train']:.3f}, val loss: {losses['val']:.3f}, elapsed time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
            self.save_model_to_pickle()
            start_time = time.time()
        # if iter % 500 == 0:
        # sample a batch of data
        xb, yb = self._get_batch('train')

        # evaluate the loss
        logits, loss = self.model.forward(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
    return loss.item()





