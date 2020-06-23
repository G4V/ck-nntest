import os
import torch
import struct
import numpy as np
import json
from pprint import pprint

dataset_path = os.environ.get('CK_DATASET_PATH', '')
dataset_file_base = os.environ.get('CK_DATASET_FILENAME', '')

alpha = float(os.environ.get('CK_GEMM_ALPHA', '1.0'))
beta  = float(os.environ.get('CK_GEMM_BETA', '0.0'))
K     = int(os.environ.get('CK_GEMM_K', '1024'))
M     = int(os.environ.get('CK_GEMM_M', '1024'))
N     = int(os.environ.get('CK_GEMM_N', '1024'))

tensors = {
    'A' : [ M, K ],
    'B' : [ K, N ],
    'C' : [ M, N ]
}

for tensor_name, tensor_shape in tensors.items():
    tensor_path = os.path.join(dataset_path, '{}.{}'.format(dataset_file_base, tensor_name))
    tensor_size = tensor_shape[0] * tensor_shape[1]
    sizeof_float = 4
    with open(tensor_path, 'rb') as tensor_file:
        tensor_as_list = struct.unpack('f'*tensor_size, tensor_file.read(sizeof_float*tensor_size))
        tensor_as_array = np.array(tensor_as_list, dtype=np.float32).reshape(tensor_shape)
        tensors[tensor_name] = torch.from_numpy(tensor_as_array)

output = alpha * torch.mm(tensors['A'], tensors['B']) + beta * tensors['C']
output_list = output.flatten().tolist()
pprint(output)

output_json = 'tmp-ck-output.json'
with open(output_json, 'w') as output_file:
    output_file.write( json.dumps(output_list, indent=2) )

output_bin = 'tmp-ck-output.bin'
with open(output_bin, 'wb') as output_file:
    output_file.write( struct.pack('f'*len(output_list), *output_list) )