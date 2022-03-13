__author__ = "sangdo.han"
import os
import glob
import librosa
import random
import copy
import numpy as np
from nptdms import TdmsFile
from librosa.feature import melspectrogram
from librosa.display import specshow
import matplotlib.pyplot as plt


def _digit_to_onehot(n_classes, digit):
    one_hot = np.zeros(n_classes)
    one_hot[digit] = 1
    return one_hot

def aug_source_dataset(filenames, 
                      labels,
                      shuffle,
                      class_names = ["NG_support_spring","OK"]):
    class_names.sort()
    stratified_dataset = { _idx:[] for _idx in range(len(class_names))}
    for fname, label in zip(filenames, labels):
        stratified_dataset[class_names.index(fname.split('/')[-2])].append([fname, label])
    cls_histogram = [len(val) for key, val in stratified_dataset.items()]
    lookup_indices, dominant_class_idx = np.argsort(cls_histogram)[:-1], np.argsort(cls_histogram)[-1]

    aug_filenames = []
    aug_labels = []
    dom_dataset = np.array(stratified_dataset[dominant_class_idx])
    aug_filenames.extend(dom_dataset[:,0].tolist())
    aug_labels.extend(dom_dataset[:,1].tolist())

    cp_dom_dataset = copy.deepcopy(dom_dataset)
    random.shuffle(cp_dom_dataset)
    
    for idx in lookup_indices:
        aug_num = cls_histogram[dominant_class_idx] - cls_histogram[idx]
        dom_participants = np.array(cp_dom_dataset[:aug_num])

        t_part = np.array(stratified_dataset[idx])
        temp_aug_dataset = copy.deepcopy(t_part)

        mixup_sets = np.array([[act_part, random.choice(t_part)] for act_part in dom_participants])
        temp_filenames = temp_aug_dataset[:,0].tolist() + mixup_sets[:,:,0].tolist()
        temp_labels = temp_aug_dataset[:,1].tolist() + mixup_sets[:,:,1].tolist()
        
        aug_filenames.extend(temp_filenames)
        aug_labels.extend(temp_labels)
       
    if shuffle:
        _zip = list(zip(aug_filenames, aug_labels))
        random.shuffle(_zip)
        aug_filenames , aug_labels = zip(*_zip)

    return list(aug_filenames), list(aug_labels)

def load_wav(file_path,sr):
    signal, _ = librosa.load(file_path, sr)
    return signal

def load_tdms(file_path, channel_name="CPsignal1"):
    """Load Single tdms file and returns target signal

    Parameters
    ----------
    file_path : str
        a single tdms file path
    channel_name : str
        Name of interest channel. Defaults to "CPsignal1".

    Returns
    --------
    np.array
        raw singal shape of (N,)
    """
    tdms_file = TdmsFile(file=file_path)
    tdms_group = tdms_file.groups()
    signal = tdms_group[0][channel_name][:]
    return signal


def get_fpaths(fpath):
    """if fpath is directory, function returns
    list of tdms files in the directory.

    Parameters
    -----------
    fpath : directory path or tdms file paths

    Raises
    ------
    FileExistsError
        if there is no file in directory
    FileExistsError
        if there is no file ends with ".tdms"

    Returns
    -------
    list
        list of tdms file paths
    """
    if isinstance(fpath, list):
        return fpath
    elif os.path.isdir(fpath):
        fpaths =[]
        fpaths.extend(glob.glob(os.path.join(fpath, "*.tdms")))
        fpaths.extend(glob.glob(os.path.join(fpath, "*.wav")))
        if fpaths:
            return fpaths
        else:
            raise FileExistsError("tdms file not exist")
    elif fpath.endswith(".tdms") or fpath.endswith(".wav"):
        return [fpath]
    else:
        raise FileExistsError("tdms file not exist")


def get_mid_signal(signal, sr=25000, window_size=2.0):
    """get middle signal with a certain time length

    Parameters
    -----------
    signal : np.array
        original signal
    sr : int
        sampling ratio. Defaults to 25000.
    window_size : float
        time window size (seconds) of output. Defaults to 2.0.
    
    Raises
    ------
    AssertionError
        if original signal is less than window_size * sr

    Returns
    -------
    np.array
        middle segment of original signal.
    """
    segment_len = int(sr * window_size)
    if len(signal) < segment_len :
        raise ValueError("original signal is inadequate about your querries,"+
            "length of signal should be larger than or equal to sr * window_size")

    mid_idx = len(signal) // 2
    start_idx = mid_idx - int(np.ceil(segment_len / 2))
    start_idx = 0 if start_idx < 0 else start_idx
    end_idx = start_idx + segment_len
    return signal[start_idx:end_idx]

def segment_signal(signal, sr=25000, hop_length=0.5, window_size=2):
    """split total signal into number of signal pieces with a certain time length

    Parameters
    -----------
    signal : np.array
        original signal
    sr : int
        sampling ratio. Defaults to 25000.
        segment .
    window_size : float
        time window size (seconds) of output. Defaults to 2.0.
    hop_length : int
        time hop size (seconds) between cosecutive signals. Defaults to 0.5
    Returns
    -------
    list
        list of signal pieces. each element is (sr * window_size) long np.array typed signal.
        length of signal pieces will be decided by hop_length and window_size.
    """
    segment_arr_len = int(sr * window_size)
    hop_arr_len = int(sr * hop_length)
    max_idx = len(signal) - segment_arr_len + 1 
    segments = [signal[offset:offset+segment_arr_len]
                for offset in range (0, max_idx ,hop_arr_len)]
    return segments

def mel_spectrogram(signal, sr, img_height, img_width):
    """Generate melody spectrogram with targeted size

    Parameters
    -----------
    signal : np.array
        1 dimensional (N,) signal
    sr : int
        sampling rate of signal
    img_height : int 
        target image height
    img_width : int 
        target image width

    Returns
    -------
    np.array
        melspectrogram. with shape of 2 dimensional numpy array
        (img_height, img_width)
    """
    hop_length = len(signal) // img_width
    n_fft = hop_length * 4 
    spec=melspectrogram(y=signal, sr=sr, n_fft=n_fft,
                        hop_length=hop_length, n_mels=img_height)
    spec= librosa.power_to_db(S=spec, ref=np.max)
    return spec[:,:img_width]

def standarize(img, norm_axis="timefreq"):
    """Normalize a Single Image by Gaussian Distribution (mean, std).

    Parameters
    -----------
    img : np.array
        a single image np array with channel last (H x W x C) 
    norm_axis : str
        name of axis that will be applied standarization.
        norm_axis should be in ["height", "freq", "width", "time", "overall", "timefreq"]
    Returns
    -------
    np.array
        standarized image
    """
    if norm_axis in ['height', "freq"]:
        img = (img - np.mean(img, axis= 1)[:, np.newaxis ,:]) / \
             np.std(img, axis= 1)[: np.newaxis, :]
    elif norm_axis in ['width', "time"]:
        img = (img - np.mean(img, axis=0)[np.newaxis, :, :]) / \
             np.std(img, axis=0)[np.newaxis, :, :]
    elif norm_axis in ['overall', "timefreq"]:
        img = (img - np.mean(img, axis=(0,1))[np.newaxis, np.newaxis, :]) / \
             np.std(img, axis=(0,1))[np.newaxis, np.newaxis, :]
    return img

def spec_to_img(spec, n_channel=3):
    """make 2d np.array to 3d np.array, the last dimension works as a channel
    i.e. original 2d np.array spectrogram (H x W) -->
    image (H x W x C), where C is equal to n_channel

    Parameters
    ----------
    spec : np.array
        2 dimensional numpy array
    n_channel : int
        number of channel, it should be 1 or 3. Defaults to 3.

    Returns
    --------
    np.array 
        dimension increased numpy array, could work as image in 
        matplotlib or tensorflow image
    """
    assert n_channel in [1,3], ValueError("n_channel should be 1 or 3")
    img_1ch = spec.reshape(*spec.shape, 1)
    if n_channel ==1 :
        return img_1ch
    else:
        img_nch = np.concatenate([img_1ch]*n_channel, axis=-1)
        return img_nch 

def _plot_spec_for_dbg(save_fname, signal, sr=25000, img_width=224, img_height=224):
    """Plot and save mel spectrogram for debug

    Parameters
    -----------
    save_fname : str 
        path of your figure
    signal : np.array
        1 dimensional numpy array contains signal amplitude information
    sr : int
        sampling ratio of signal. Defaults to 25000
    img_width : int
        width of image/spectrogram. Defaults to 224.
    img_height : int
        height of image/spectrogram. Defaults to 224.
    """
    plt.figure()
    spec = mel_spectrogram(signal, sr, img_width=img_width, img_height=img_height)
    img = specshow(spec, sr=sr, hop_length=len(signal)/img_width, x_axis='time')
    save_fname = save_fname.rstrip('.png')
    plt.savefig(f"{save_fname}.png")

def make_dataset(dataset_top_dir):
    files = []
    labels = []
    classes = os.listdir(dataset_top_dir)
    classes.sort()
    n_classes = len(classes)
    for idx, _cls in enumerate(classes):
        one_hot = np.zeros(n_classes)
        one_hot[idx] = 1
        one_hots = [one_hot]
        _files = glob.glob(
            os.path.join(os.path.join(dataset_top_dir, _cls), "*.*")
        )
        files.extend(_files)
        labels.extend(one_hots * len(_files))
    return files, labels