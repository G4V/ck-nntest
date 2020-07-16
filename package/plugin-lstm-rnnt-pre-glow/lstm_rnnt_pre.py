import torch
import os
import numpy as np
from torch import nn
from typing import Optional, Tuple
import time

import ctypes
import numpy.ctypeslib as ctl

plugin_dir      = "PLUGIN_DIR"
embedding_width = int("EMBEDDING_WIDTH")
hidden_width    = int("HIDDEN_WIDTH")
num_layers      = int("NUM_LAYERS")

class PluginLstmRnntPre(torch.nn.Module):
    def __init__(self):
        super().__init__()

        print("---------------------------")
        print("LOADING RNNT LSTM PRE: GLOW")
        print("---------------------------")

        self.libc = ctypes.CDLL(plugin_dir + "/model.so")
        self.lstm = self.libc.lstm

        self.lstm.argtypes = [ctl.ndpointer(np.float32),#, flags='aligned, c_contiguous'),
                              ctypes.c_int,
                              ctl.ndpointer(np.float32),#, flags='aligned, c_contiguous'),
                              ctl.ndpointer(np.float32),#, flags='aligned, c_contiguous'),
                              ctl.ndpointer(np.float32),#, flags='aligned, c_contiguous'),
                              ctl.ndpointer(np.float32),#, flags='aligned, c_contiguous'),
                              ctl.ndpointer(np.float32)]#, flags='aligned, c_contiguous')]

        self.zeros_h_0 = np.zeros([num_layers,1,hidden_width], dtype=np.float32)
        self.zeros_c_0 = np.zeros([num_layers,1,hidden_width], dtype=np.float32)

    def forward(self, x: torch.Tensor, 
                init_states: Optional[Tuple[torch.Tensor]]=None
               ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:

        logits = x.size()[0]
        # Convert the inputs to Numpy and float32
        xin = x.numpy().astype(np.float32)
        if init_states:
            h_0 = init_states[0].np().astype(np.float32)
            c_0 = init_states[1].np().astype(np.float32)
        else:
            h_0 = self.zeros_h_0
            c_0 = self.zeros_c_0

        out = np.empty([logits,1,hidden_width], dtype=np.float32, order='C')
        h_n = np.empty([num_layers,1,hidden_width], dtype=np.float32, order='C')
        c_n = np.empty([num_layers,1,hidden_width], dtype=np.float32, order='C')

        start = time.time()
        self.lstm(xin, logits, h_0, c_0, out, h_n, c_n)
        print("time taken %f" % (time.time() - start))

        out = torch.from_numpy(out)
        h_n = torch.from_numpy(h_n)
        c_n = torch.from_numpy(c_n)

        return out, (h_n, c_n)




'''
test = PluginLstmRnntPre()

hello = torch.ones([100,1,240], dtype=torch.float32)

test.forward(hello, None)

print("no crash!!!")
'''

