import librosa
import librosa.display
import pydub
import matplotlib.pyplot as plt
import numpy as np

def dubread(filename):
    #a = pydub.AudioSegment.from_file(file=filename, format='wav')
    # if .mp3 in filename...
    if '.mp3' in filename:
        a = pydub.AudioSegment.from_file(file=filename, format='mp3')
    else:
        a = pydub.AudioSegment.from_file(file=filename, format='wav')

    channel_sounds = a.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]
    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max

    y, sr = fp_arr[:, 0], a.frame_rate
    return y, sr
  
def plot_spec(y,sr):
    D = librosa.stft(y)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots(figsize=(8,3))
    img = librosa.display.specshow(S_db, x_axis="time", y_axis="linear", ax=ax)
    # ax.set(title=transformation_name)
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    return plt.gcf()

def plot_wave(y,sr):
    fig, ax = plt.subplots(figsize=(8,3))
    img = librosa.display.waveshow(y, sr=sr, x_axis="time", ax=ax)
    return plt.gcf()
