import random
import os
from glob import glob
import importlib
from pysrc import const
import argparse


def get_wav_files_train_test(train_rate=0.8):
    files = glob(os.path.join(const.DATA_DIR, '*.wav'))
    random.shuffle(files)
    n = len(files)
    train_list, test_list = files[0:int(n * train_rate)], files[int(n * train_rate):]
    with open('data/train.txt', 'w') as f:
        for file in train_list:
            f.write(file)
            f.write('\n')
    with open('data/test.txt', 'w') as f:
        for file in test_list:
            f.write(file)
            f.write('\n')


if __name__ == '__main__':
    get_wav_files_train_test()
