import time as _time
from pysrc.networks import ResModel as _net

_name = 'resnet'
_time = _time.strftime('%m-%d %H:%M:%S', _time.localtime())

USE_NET = _net

TRAIN_DIR = 'runs/%s/' % _name + _time
VAL_DIR = 'runs/%s/' % _name + _time

MODEL_NAME = '%s.pkl' % _name

BATCH_SIZE = 16
VAL_BATCH_SIZE = 16