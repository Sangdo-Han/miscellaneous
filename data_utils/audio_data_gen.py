__author__ = "sangdo.han"
import math
import keras
import random
import numpy as np
import matplotlib.pyplot as plt
from .utils import (spec_to_img, 
                    load_wav, 
                    load_tdms, 
                    get_mid_signal, 
                    segment_signal, 
                    mel_spectrogram,
                    standarize,
                    spec_to_img)

class ArcFaceGenerator(keras.utils.Sequence):
    def __init__(self,
            filenames,
            labels,
            channel_name="CPsignal1",
            time_size=2,
            sr=25000,
            img_height=224,
            img_width=224,
            batch_size=32,
            mixup_alpha=0.5,
            mixup_beta=0.5,
            mixup_margin=1e-5,
            shuffle=False):
    
        if shuffle:
            _zip = zip(filenames, labels)
            random.shuffle(_zip)
            filenames, labels = zip(*_zip)
            self.filenames = list(filenames)
            self.labels = list(labels)
        else:
            self.filenames = filenames
            self.labels = labels

        self.sr = sr
        self.time_size = time_size
        self.img_height = img_height
        self.img_width = img_width
        self.channel_name = channel_name
        self.batch_size = batch_size

        self.mixup_alpha = mixup_alpha
        self.mixup_beta = mixup_beta
        self.min_lam = 0.0 + mixup_margin
        self.max_lam = 1.0 - mixup_margin

    def _get_specs(self, fpath):
        _signal = self._get_signal(fpath)
        mid_signal = get_mid_signal(_signal,self.sr,self.time_size)
        _spec = mel_spectrogram(mid_signal,self.sr,self.img_height,self.img_width)
        spec_img = spec_to_img(_spec, n_channel=3)
        spec_img = standarize(spec_img, norm_axis="timefreq")
        return spec_img

    def _get_signal(self, fpath):
        if fpath.endswith('tdms'):
            _signal = load_tdms(file_path=fpath,
                                    channel_name=self.channel_name)
        else:
            _signal = load_wav(file_path=fpath, sr=self.sr)
        return _signal

    def __len__(self):
        return math.ceil(int(len(self.filenames)/self.batch_size))

    def __getitem__(self, index):
        # _mb means in mini batch
        logits_mb = []
        fpaths_mb = self.filenames[index*self.batch_size:(index+1)*self.batch_size]
        y = self.labels[index*self.batch_size:(index+1)*self.batch_size]
        for idx, fpath in enumerate(fpaths_mb):
            if isinstance(fpath, list):
                spec_img1 = self._get_specs(fpath[0])
                spec_img2 = self._get_specs(fpath[1])
                lam = np.random.beta(self.mixup_alpha, self.mixup_beta)
                lam = np.clip(lam, self.min_lam, self.max_lam)
                spec_img = (1-lam) * spec_img1 + lam * spec_img2
                y[idx] = (1-lam) * y[idx][0] + lam * y[idx][1]
            else:
                spec_img = self._get_specs(fpath)
            logits_mb.append(spec_img)

        X = np.array(logits_mb)
        y = np.array(y)
        return [X, y], y

class FileBasedTrainGenerator(keras.utils.Sequence):
    def __init__(self,
            filenames,
            labels,
            channel_name="CPsignal1",
            time_size=2,
            sr=25000,
            img_height=224,
            img_width=224,
            batch_size=32,
            mixup_alpha=2,
            mixup_beta=8,
            mixup_margin=1e-5,
            shuffle=False):
    
        if shuffle:
            _zip = zip(filenames, labels)
            random.shuffle(_zip)
            filenames, labels = zip(*_zip)
            self.filenames = list(filenames)
            self.labels = list(labels)
        else:
            self.filenames = filenames
            self.labels = labels

        self.sr = sr
        self.time_size = time_size
        self.img_height = img_height
        self.img_width = img_width
        self.channel_name = channel_name
        self.batch_size = batch_size

        self.mixup_alpha = mixup_alpha
        self.mixup_beta = mixup_beta
        self.min_lam = 0.5 + mixup_margin
        self.max_lam = 1.0 - mixup_margin

    def _get_specs(self, fpath):
        _signal = self._get_signal(fpath)
        mid_signal = get_mid_signal(_signal,self.sr,self.time_size)
        _spec = mel_spectrogram(mid_signal,self.sr,self.img_height,self.img_width)
        spec_img = spec_to_img(_spec, n_channel=3)
        spec_img = standarize(spec_img, norm_axis="timefreq")
        return spec_img

    def _get_signal(self, fpath):
        if fpath.endswith('tdms'):
            _signal = load_tdms(file_path=fpath,
                                    channel_name=self.channel_name)
        else:
            _signal = load_wav(file_path=fpath, sr=self.sr)
        return _signal

    def __len__(self):
        return math.ceil(int(len(self.filenames)/self.batch_size))

    def __getitem__(self, index):
        # _mb means in mini batch
        logits_mb = []
        fpaths_mb = self.filenames[index*self.batch_size:(index+1)*self.batch_size]
        y = self.labels[index*self.batch_size:(index+1)*self.batch_size]
        for idx, fpath in enumerate(fpaths_mb):
            if isinstance(fpath, list):
                spec_img1 = self._get_specs(fpath[0])
                spec_img2 = self._get_specs(fpath[1])
                lam = np.random.beta(self.mixup_alpha, self.mixup_beta)
                lam = np.clip(lam, self.min_lam, self.max_lam)
                spec_img = (1-lam) * spec_img1 + lam * spec_img2
                y[idx] = (1-lam) * y[idx][0] + lam * y[idx][1]
            else:
                spec_img = self._get_specs(fpath)
            logits_mb.append(spec_img)

        X = np.array(logits_mb)
        y = np.array(y)
        return X, y

class FileBasedPredGenerator(keras.utils.Sequence):
    def __init__(self, filenames, channel_name, sr, time_size, img_height, img_width, batch_size):
        self.filenames = filenames
        self.batch_size = batch_size
        self.sr = sr
        self.time_size = time_size
        self.img_height = img_height
        self.channel_name = channel_name
        self.img_width = img_width
    def __len__(self):
        return math.ceil(int(len(self.filenames)/self.batch_size))
    def __getitem__(self, index):
        img_list = []
        fpaths = self.filenames[index*self.batch_size:(index+1)*self.batch_size]
        for fpath in fpaths:
            if fpath.endswith('tdms'):
                _signal = load_tdms(file_path=fpath,
                                            channel_name=self.channel_name)
            else:
                _signal = load_wav(file_path=fpath, sr=self.sr)
            mid_signal = get_mid_signal(_signal,self.sr,self.time_size)
            _spec = mel_spectrogram(mid_signal,self.sr,self.img_height,self.img_width)
            spec_img = spec_to_img(_spec, n_channel=3)
            spec_img = standarize(spec_img, norm_axis="timefreq")
            img_list.append(spec_img)
        X = np.array(img_list)
        return X

class LogitBasedPredGenerator(keras.utils.Sequence):
    def __init__(self, logits, batch_size=1) -> None:
        self.X = logits
        self.batch_size=batch_size
    def __len__(self):
        return math.ceil(int(self.X.shape[0])/self.batch_size)
    def __getitem__(self, index):
        return self.X[index*self.batch_size: (index+1)*self.batch_size, :]
