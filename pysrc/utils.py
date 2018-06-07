import random
import os
from glob import glob
import importlib
from pysrc import const
import argparse


def merge_const(module_name):
    new_conf = importlib.import_module(module_name)
    for key, value in new_conf.__dict__.items():
        if not(key.startswith('_')):
            # const.__dict__[key] = value
            setattr(const, key, value)
            print('override', key, value)


def parse_args_and_merge_const():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', default='', type=str)
    args = parser.parse_args()
    if args.conf != '':
        merge_const(args.conf)


def get_train_list():
    with open(const.TRAIN_LIST) as f:
        return [x.strip() for x in f]


def get_test_list():
    with open(const.TEST_LIST) as f:
        return [x.strip() for x in f]
