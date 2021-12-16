import os.path
from pathlib import Path

import librosa.display
from matplotlib.figure import Figure
import matplotlib
import librosa as lr


def make_plot(audio_file, resampled_audio_file, original_sample_rate, modified_sample_rate):
    """" Produce a plot comparing the waveform before and after resampling
    """""
    basename = Path(audio_file).stem
    audio, sample_rate = lr.load(audio_file, sr=original_sample_rate)
    resampled_audio, resampled_rate = lr.load(resampled_audio_file, sr=modified_sample_rate)

    # Set up for making a plot
    fig = matplotlib.figure.Figure()
    ax, ax2 = fig.subplots(nrows=2)

    # Display the wave form using librosa
    librosa.display.waveshow(audio, sr=original_sample_rate, ax=ax, marker='.', label='Default', color='b')
    librosa.display.waveshow(resampled_audio, sr=modified_sample_rate, ax=ax2, marker='.', label='Resampled',
                             color='r')
    ax.label_outer()
    ax.legend()
    ax2.legend()

    image = os.path.join('templates/images/Resample_' + basename + '.png')
    fig.savefig(image)
    return image
