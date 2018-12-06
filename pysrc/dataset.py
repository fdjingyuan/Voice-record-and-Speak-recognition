import torch
import torch.utils.data
import numpy as np
# import matplotlib.pyplot as plt
# from skimage import io, transform
from pysrc import const
import random
import librosa
from scipy import signal
import IPython.display as ipd
from glob import glob
import cv2


class Audio(object):

    def __init__(self, filename=None, sr=const.SR, second=None, samples=None):
        '''
        filename: 音频文件名
        sr：resample到的sample rate
        second: 会被crop或pad到这个秒数
        '''
        if samples is None:
            samples, sample_rate = librosa.load(filename, sr=sr)
            assert sample_rate == sr
        else:
            assert filename is None
        self.sr = sr
        if second is not None and len(samples) < sr * second:
            samples = np.pad(samples, (0, sr * second - len(samples)), 'constant')
        if second is not None and len(samples) > sr * second:
            samples = samples[0:sr * second]
        self.samples = samples

    def mfcc_feature(self, resize=None):
        spectrogram = librosa.feature.melspectrogram(self.samples, sr=self.sr, n_mels=40, hop_length=160, n_fft=480, fmin=20, fmax=4000)
        idx = [spectrogram > 0]
        spectrogram[idx] = np.log(spectrogram[idx])

        dct_filters = librosa.filters.dct(n_filters=40, n_input=40)
        mfcc = [np.matmul(dct_filters, x) for x in np.split(spectrogram, spectrogram.shape[1], axis=1)]
        mfcc = np.hstack(mfcc)
        mfcc = mfcc.astype(np.float32)
        if resize:
            mfcc = cv2.resize(mfcc, (resize, resize))
        return mfcc

    def mel_feature(self, n_mels=40, normalization=False, resize=None):
        spectrogram = librosa.feature.melspectrogram(self.samples, sr=self.sr, n_mels=n_mels, hop_length=160, n_fft=480, fmin=20, fmax=4000)
        spectrogram = librosa.power_to_db(spectrogram)
        spectrogram = spectrogram.astype(np.float32)
        if normalization:
            spectrogram = spectrogram.spectrogram()
            spectrogram -= spectrogram
        if resize:
            # spectrogram = transform.resize(spectrogram, (resize, resize), preserve_range=True, mode='reflect')
            spectrogram = cv2.resize(spectrogram, (resize, resize))
        return spectrogram

    def plot_specgram(self, window_size=20, step_size=10, eps=1e-10):
        def log_specgram(audio, sample_rate, window_size=20,
                         step_size=10, eps=1e-10):
            nperseg = int(round(window_size * sample_rate / 1e3))
            noverlap = int(round(step_size * sample_rate / 1e3))
            freqs, times, spec = signal.spectrogram(audio,
                                                    fs=sample_rate,
                                                    window='hann',
                                                    nperseg=nperseg,
                                                    noverlap=noverlap,
                                                    detrend=False)
            return freqs, times, np.log(spec.T.astype(np.float32) + eps)

        freqs, times, spectrogram = log_specgram(self.samples, self.sr)

        fig = plt.figure(figsize=(14, 8))
        ax1 = fig.add_subplot(211)
        ax1.set_title('Raw wave')
        ax1.set_ylabel('Amplitude')
        ax1.plot(np.linspace(0, self.sr / len(self.samples), self.sr), self.samples)

        ax2 = fig.add_subplot(212)
        ax2.imshow(spectrogram.T, aspect='auto', origin='lower',
                   extent=[times.min(), times.max(), freqs.min(), freqs.max()])
        ax2.set_yticks(freqs[::16])
        ax2.set_xticks(times[::16])
        ax2.set_title('Spectrogram')
        ax2.set_ylabel('Freqs in Hz')
        ax2.set_xlabel('Seconds')

    def play(self):
        return ipd.Audio(data=self.samples, rate=self.sr, autoplay=True)

    def timeshift(self, wav, ms=100):
        shift = (self.sr * ms) // 1000
        shift = random.randint(-shift, shift)
        a = -min(0, shift)
        b = max(0, shift)
        data = np.pad(wav, (a, b), "constant")
        return data[:len(data) - a] if a else data[b:]

    def noise(self, noise_files):
        scale = random.uniform(0.75, 1.25)
        num_noise = random.choice([1, 2])
        max_ratio = random.choice([0.2, 0.5, 1, 1.2])
        shift_range = random.randint(320, 480)
        length = len(self.samples)
        samples = scale * (self.timeshift(self.samples, shift_range) +
                           self.get_mix_noises(noise_files, length, num_noise, max_ratio))
        return Audio(sr=self.sr, samples=samples)

    def get_one_noise(self, noise_files, length):
        selected_noise = noise_files[random.randint(0, len(noise_files) - 1)]
        start_idx = random.randint(0, len(selected_noise) - 1 - length)
        return selected_noise[start_idx:(start_idx + length)]

    def get_mix_noises(self, noise_files, length, num_noise=1, max_ratio=0.1):
        result = np.zeros(length)
        for _ in range(num_noise):
            result += random.random() * max_ratio * self.get_one_noise(noise_files, length)
        return result / num_noise if num_noise > 0 else result


class FudanVoiceDataset(torch.utils.data.Dataset):

    def __init__(self, file_list, noise_ratio, norm=True):
        self.sr = const.SR
        self.noise_files = [librosa.load(x, sr=self.sr)[0] for x in glob(const.NOISE_DIR + '*.wav')]
        self.file_list = file_list
        self.noise_ratio = noise_ratio
        self.norm = norm

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        filename = self.file_list[idx]
        audio = Audio(filename, self.sr)

        if random.random() < self.noise_ratio:
            audio = audio.noise(self.noise_files)

        sample = {}
        # sample['data'] = audio.samples
        sample['mfcc'] = audio.mfcc_feature(resize=const.FEATURE_SIZE)
        sample['mel'] = audio.mel_feature(resize=const.FEATURE_SIZE)
        if self.norm:
            sample['mfcc'] = (sample['mfcc'] - const.MFCC_MEAN) / const.MFCC_STD
            sample['mel'] = (sample['mel'] - const.MEL_MEAN) / const.MEL_STD
        sample['label'] = torch.tensor(int(filename.split('-')[-2]), dtype=torch.int64)
        sample['mfcc'] = sample['mfcc'].astype(np.float32)
        sample['mel'] = sample['mel'].astype(np.float32)
        sample['mfcc'] = sample['mfcc'][np.newaxis, :, :]
        sample['mel'] = sample['mel'][np.newaxis, :, :]
        # sample['audio'] = audio
        return sample
