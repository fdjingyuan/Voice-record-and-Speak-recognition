import torch
import torch.nn.functional as F
import torch.nn as nn
import math
from torch.nn import MaxPool2d

class ModuleWithAttr(nn.Module):

    # 只能是数字，默认注册为0

    def __init__(self, extra_info=['step']):
        super(ModuleWithAttr, self).__init__()
        for key in extra_info:
            self.set_buffer(key, 0)

    def set_buffer(self, key, value):
        if not(hasattr(self, '__' + key)):
            self.register_buffer('__' + key, torch.tensor(value))
        setattr(self, '__' + key, torch.tensor(value))

    def get_buffer(self, key):
        if not(hasattr(self, '__' + key)):
            raise Exception('no such key!')
        return getattr(self, '__' + key).item()


class VGG(ModuleWithAttr):

    def __init__(self, features):
        super(VGG, self).__init__()
        n_labels = 20
        self.features = features
        self.classifier = nn.Sequential(
            nn.Linear(256 * 2, 1024),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(1024, 256),
            nn.ReLU(True),
            nn.Dropout(0.25),
            nn.Linear(256, n_labels),
        )

    def forward(self, x):
        x = self.features(x)
        max_x = F.adaptive_max_pool2d(x, (1, 1))
        avg_x = F.adaptive_avg_pool2d(x, (1, 1))
        x = torch.cat([max_x, avg_x], 1)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def make_layers(cfg, batch_norm=True, ks=3, kp=1):
    layers = []
    in_channels = 1
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=ks, padding=kp)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


def vgg2d():
    """VGG 16-layer model with batch normalization"""
    return VGG(make_layers([64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 256, 256, 256, 'M']))

def vgg2d_thin():
    return VGG(make_layers([32, 32, 'M', 64, 64, 'M', 128, 128, 128, 'M', 256, 256, 256, 'M', 128, 128, 256, 'M']))

class ResModel(ModuleWithAttr):
    def __init__(self):
        super(ResModel, self).__init__()
        n_labels = 20
        n_maps = 128
        self.conv0 = torch.nn.Conv2d(1, n_maps, (3, 3), padding=(1, 1), bias=False)
        self.n_layers = n_layers = 9
        self.convs = torch.nn.ModuleList([torch.nn.Conv2d(n_maps, n_maps, (3, 3), padding=1, dilation=1,
                                                          bias=False) for _ in range(n_layers)])
        self.pool = MaxPool2d(2, return_indices=True)
        for i, conv in enumerate(self.convs):
            self.add_module("bn{}".format(i + 1), torch.nn.BatchNorm2d(n_maps, affine=False))
            self.add_module("conv{}".format(i + 1), conv)
        self.output = torch.nn.Linear(n_maps, n_labels)

    def forward(self, x):
        for i in range(self.n_layers + 1):
            y = F.relu(getattr(self, "conv{}".format(i))(x))
            if i == 0:
                old_x = y
            if i > 0 and i % 2 == 0:
                x = y + old_x
                old_x = x
            else:
                x = y
            if i > 0:
                x = getattr(self, "bn{}".format(i))(x)
            pooling = False
            if pooling:
                x_pool, pool_indices = self.pool(x)
                x = self.unpool(x_pool, pool_indices, output_size=x.size())
        x = x.view(x.size(0), x.size(1), -1)
        x = torch.mean(x, 2)
        return self.output(x)
