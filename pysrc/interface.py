from pysrc import const
from pysrc.dataset import Audio
import numpy as np
from pysrc.utils import parse_args_and_merge_const
import torch
import torch.nn.functional as F


class WavRecgnition(object):

    def __init__(self, use_device='cpu'):
        print('load net...')
        net = const.USE_NET()
        net = net.to(const.device)
        net.load_state_dict(torch.load('models/' + const.MODEL_NAME, map_location={'cuda:0': use_device}))
        net.eval()
        self.net = net
        print('ok..')

    def classify(self, samples):
        audio = Audio(samples=samples)
        mel = audio.mel_feature(resize=const.FEATURE_SIZE)
        mel = (mel - const.MEL_MEAN) / const.MEL_MEAN
        mel = mel.astype(np.float32)
        # 通道和batch
        mel = mel[np.newaxis, np.newaxis, :, :]
        mel = torch.from_numpy(mel)
        output = self.net(mel)
        _, predicted = torch.max(output.data, 1)
        prob = F.softmax(output, dim=1)
        print('prob:')
        print(prob.detach().cpu().numpy())
        predicted = predicted.detach().cpu().numpy()[0]
        prob = prob[0, predicted].item()
        return const.TOKENS[predicted], prob


if __name__ == '__main__':
    import librosa
    parse_args_and_merge_const()
    interface = WavRecgnition()
    samples, _ = librosa.load('data/raw/13307130239-01-02.wav', sr=const.SR)
    print(interface.classify(samples))


