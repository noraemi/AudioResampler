import os.path
from io import BytesIO
from pathlib import Path

import librosa.display
import matplotlib
# import matplotlib.figure as Figure
import librosa as lr


RESAMPLE_FOLDER = 'RESAMPLE_FOLDER/'


def make_plot(file, resampled_file, org_sr, resample_rate):
    basename = Path(file).stem
    audio, sr = lr.load(file, org_sr)
    raudio, rsr = lr.load(resampled_file, resample_rate)

    # Set up for making a plot
    fig = matplotlib.figure.Figure()
    print('cookie')
    ax, ax2 = fig.subplots(nrows=2)
    print('hi')
    librosa.display.waveshow(audio, sr=sr, ax=ax, marker='.', label='Default', color='b')
    librosa.display.waveshow(raudio, sr=resample_rate, ax=ax2, marker='.', label='Resampled',
                             color='r')
    ax.label_outer()
    ax.legend()
    ax2.legend()

    image = os.path.join('templates/images/Resample_' + basename + '.png')
    # buf = BytesIO()
    print('saving plot')
    fig.savefig(image)
    print('Made image')
    return image
