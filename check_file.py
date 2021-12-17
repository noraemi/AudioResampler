import sys
from pydub.utils import mediainfo


def check_media_sample_rate(filename):
    """Get meta data info from a media file
    """
    try:
        info = mediainfo(filename)
    except BaseException:
        raise Exception('Failed to extract media information from file')
    sample_rate_file = int(info['sample_rate'])
    print('File has sample rate {}\n'.format(sample_rate_file))


if __name__ == '__main__':
    args = sys.argv[1]
    check_media_sample_rate(args)
