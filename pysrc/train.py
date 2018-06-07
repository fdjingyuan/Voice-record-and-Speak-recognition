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


if __name__ == '__main__':
    parse_args_and_merge_const()
    if os.path.exists('models') is False:
        os.makedirs('models')

    train_list, test_list = get_train_list(), get_test_list()
    train_dataset = FudanVoiceDataset(train_list, const.NOISE_RATIO, const.NORM_DATA)
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=const.BATCH_SIZE, shuffle=True, num_workers=4)
    test_dataset = FudanVoiceDataset(test_list, 0, const.NORM_DATA)
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=const.VAL_BATCH_SIZE, shuffle=True, num_workers=4)

    net = const.USE_NET()
    net = net.to(const.device)

    learning_rate = const.LEARNING_RATE
    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)

    writer = SummaryWriter(const.TRAIN_DIR)

    total_step = len(train_dataloader)
    step = 0
    criterion = nn.CrossEntropyLoss()
    for epoch in range(const.NUM_EPOCH):
        net.train()
        for i, sample in enumerate(train_dataloader):
            step += 1
            for key in sample:
                sample[key] = sample[key].to(const.device)
            output = net(sample['mel'])
            loss = criterion(output, sample['label'])

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 10 == 0:
                writer.add_scalar('loss', loss.item(), step)
                writer.add_scalar('learning_rate', learning_rate, step)
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, const.NUM_EPOCH, i + 1, total_step, loss.item()))

        print('Saving Model....')
        net.set_buffer('step', step)
        torch.save(net.state_dict(), 'models/' + const.MODEL_NAME)
        print('OK. Now evaluate..')

        net.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
        with torch.no_grad():
            correct = 0
            total = 0
            for i, sample in enumerate(test_dataloader):
                for key in sample:
                    sample[key] = sample[key].to(const.device)
                output = net(sample['mel'])
                _, predicted = torch.max(output.data, 1)
                total += sample['label'].size(0)
                correct += (predicted == sample['label']).sum().item()

            print('Test Accuracy: {:.2f}%'.format(100 * correct / total))
            writer.add_scalar('accuracy', correct / total, step)
        # learning rate decay
        learning_rate *= const.LEARNING_RATE_DECAY
        optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
