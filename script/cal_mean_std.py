from pysrc.dataset import FudanVoiceDataset
import torch
import torch.utils.data
from torch import nn
import numpy as np
from torch.nn import functional as F
from pysrc import const
from pysrc.utils import parse_args_and_merge_const, get_train_list, get_test_list
from tensorboardX import SummaryWriter
import os

train_list, test_list = get_train_list(), get_test_list()
d = FudanVoiceDataset(train_list + test_list, const.NOISE_RATIO, norm=False)

mfccs = []
mels = []
for i in range(len(d)):
    sample = d[i]
    mfccs.append(sample['mfcc'].reshape(-1))
    mels.append(sample['mel'].reshape(-1))
    if i % 100 == 0:
        print(i)

mfccs = np.array(mfccs)
mels = np.array(mels)

print(mfccs.mean())
print(mfccs.std())
print(mels.mean())
print(mels.std())
