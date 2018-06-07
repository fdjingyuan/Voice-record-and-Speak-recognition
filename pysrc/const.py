import time as _time
import torch as _torch
from pysrc.networks import vgg2d as _net

_name = 'vgg'
_time = _time.strftime('%m-%d %H:%M:%S', _time.localtime())

USE_NET = _net

TRAIN_DIR = 'runs/%s/' % _name + _time
VAL_DIR = 'runs/%s/' % _name + _time

MODEL_NAME = '%s.pkl' % _name

DATA_DIR = './data/raw/'
NOISE_DIR = './data/noise/'

FEATURE_SIZE = 128

SR = 16000

device = _torch.device('cuda:0' if _torch.cuda.is_available() else 'cpu')

NOISE_RATIO = 0.5

BATCH_SIZE = 32
VAL_BATCH_SIZE = 32

LEARNING_RATE = 0.001
NUM_EPOCH = 50
LEARNING_RATE_DECAY = 0.98

TRAIN_LIST = 'data/train.txt'
TEST_LIST = 'data/test.txt'

NORM_DATA = True

MEL_MEAN = -36.710186191518034
MEL_STD = 20.10469803302708
MFCC_MEAN = -1.0045979888614194
MFCC_STD = 7.631767213246153

TOKENS = ['语音', '余音', '识别', '失败', '中国',
          '忠告', '北京', '背景', '上海', '商行',
          '复旦', '饭店', 'Speech', 'Speaker', 'Signal',
          'File', 'Print', 'Open', 'Close', 'Project']
assert len(TOKENS) == 20

