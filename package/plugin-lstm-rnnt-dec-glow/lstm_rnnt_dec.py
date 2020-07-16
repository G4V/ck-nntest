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

class PluginLstmRnntDec(torch.nn.Module):
    def __init__(self):
        super().__init__()

        print("---------------------------")
        print("LOADING RNNT LSTM DEC: GLOW")
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
            h_0 = init_states[0].numpy().astype(np.float32)
            c_0 = init_states[1].numpy().astype(np.float32)
        else:
            h_0 = self.zeros_h_0
            c_0 = self.zeros_c_0

        out = np.empty([logits,1,hidden_width], dtype=np.float32)
        h_n = np.empty([num_layers,1,hidden_width], dtype=np.float32)
        c_n = np.empty([num_layers,1,hidden_width], dtype=np.float32)

        start = time.time()
        print("pyin %f %f %f" % (xin[0][0][0], xin[0][0][1], xin[0][0][2]))
        print("pyh %f %f %f" % (h_0[0][0][0], h_0[0][0][1], h_0[0][0][2]))
        print("pyc %f %f %f" % (c_0[0][0][0], c_0[0][0][1], c_0[0][0][2]))
        self.lstm(xin, logits, h_0, c_0, out, h_n, c_n)
        print("opy %f %f %f" % (out[0][0][0], out[0][0][1], out[0][0][2]))
        print("opyh %f %f %f" % (h_n[0][0][0], h_n[0][0][1], h_n[0][0][2]))
        print("opyc %f %f %f" % (c_n[0][0][0], c_n[0][0][1], c_n[0][0][2]))
        print("time taken %f\n\n\n" % (time.time() - start))

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

