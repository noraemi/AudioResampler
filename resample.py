import os.path
import uuid
from pathlib import Path

from pydub import AudioSegment
from pydub.utils import mediainfo

import plotter


def process_audio_file(filename, resample_rate, do_plot, directory):
    """Resamples the input file using pydub to change the frame-rate and export the modified file.
    Option available to produce a validation plot showing the difference in the end result.
    """
    try:
        info = mediainfo(filename)
    except BaseException:
        raise Exception('Failed to extract media information from file')

    sample_rate_file = int(info['sample_rate'])
    channels = info['channels']
    codec = info['codec_name']

    print('Sample rate: {}, Channels: {}, Codec: {}'.format(sample_rate_file, channels, codec))

    # Only supported formats mp3 and wav
    # Should work with few more from soundfile library: ogg, flac, ...?
    if not (codec == 'mp3' or codec == 'wav'):
        raise Exception('Unsupported codec type \'{}\''.format(codec))

    # No point to continue if the original file is of worse quality
    if sample_rate_file <= resample_rate:
        raise Exception('Sample frequency already less than {}'.format(resample_rate))

    # Load and set the new frame rate / sample rate and export the new file
    converted_file = ''
    try:
        converted_file = AudioSegment.from_file(filename, format=codec)
        converted_file = converted_file.set_frame_rate(resample_rate)
    except Exception as e:
        raise Exception('AudioSegment failed')
    new_filename = os.path.join(directory, str(uuid.uuid4()) + '.mp3')
    converted_file.export(new_filename, format='mp3')

    # Make a plot showing the original versus the resampled file
    image_name = ''
    if do_plot == 'True':
        try:
            image_name = plotter.make_plot(filename, new_filename, sample_rate_file, resample_rate)
        except Exception as ex:
            raise Exception('Problems with making the plot')

    resampled_info = mediainfo(new_filename)
    print(resampled_info)
    resampled_sr = resampled_info['sample_rate']
    resampled_channels = resampled_info['channels']
    print('Resample rate: {}, Channels: {}'.format(resampled_sr, resampled_channels))

    return [Path(new_filename).name, image_name]