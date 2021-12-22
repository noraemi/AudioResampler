import os
import uuid

from flask import Flask, render_template, request, send_from_directory, current_app, Response
import werkzeug
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from resample import process_audio_file
import logging

# TODO set up deletion of the temporary file

# Set up the app and configure it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESAMPLE_FOLDER'] = 'resamples'
app.config['IMAGE_FOLDER'] = 'templates/images'

# Set up logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Variables needed
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
DEFAULT_SAMPLE_FREQUENCY = '32000'
ALLOWED_FREQUENCIES = [16000, 22050, 32000, 44100, 48000]


def allowed_file(filename):
    """Initial check if file is valid depending on the file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello!!'


@app.route('/resampler/')
def resample():
    """Landing page for uploading file via web-browser
    Takes the allowed sample rates as input to generate the web-form
    """
    return render_template('upload.html', sample_rate_list=ALLOWED_FREQUENCIES)


def process_request():
    """Read parameters from the POST request and call process_audio_file() from resample.py to return the resampled
    file together with an image if requested
    """
    if not os.path.isdir(app.config['RESAMPLE_FOLDER']):
        os.mkdir(app.config['RESAMPLE_FOLDER'])
    file = request.files['file']
    filename = os.path.join(app.config['RESAMPLE_FOLDER'], secure_filename(str(uuid.uuid4())))
    file.save(filename)
    logging.debug('Saving file {}'.format(filename))
    if file.filename == '':
        logging.info('File is missing')
        return redirect()
    elif not (file and allowed_file(file.filename)):
        logging.info('Invalid file {}'.format(file.filename))
        return redirect()

    resample_frequency = request.form.get('resample_rate')
    if resample_frequency is None:
        logging.debug('Setting resampling target frequency to default value')
        resample_frequency = DEFAULT_SAMPLE_FREQUENCY

    logging.debug('Resampling target frequency {}'.format(resample_frequency))

    do_plot = request.form.get('make_plot')
    if not do_plot:
        do_plot = 'False'
    else:
        logging.debug('Plot requested')

    new_file = ''
    image = ''
    try:
        new_file, image = process_audio_file(filename, int(resample_frequency), do_plot, app.config['RESAMPLE_FOLDER'])
    except Exception as ex:
        return handle_bad_request(ex)

    return new_file, image


@app.route('/resampler/audio/', methods=['POST'])
def resample_audio():
    """Process the uploaded file and returns the resampled files in bytes to client.
    """
    logging.debug('resample_audio(): Resampling audio and returning the bytes')
    new_file, image = process_request()
    file = open(new_file, "rb")
    return file.read()


@app.route('/resampler/audio/file', methods=['POST', 'GET'])
def resample_audio_file():
    """Process the uploaded file and prompts directly with a file-download to the client for web-usage.
    """
    new_file, image = process_request()
    return load_file(new_file)


@app.route('/resampler/audio/file_and_image', methods=['POST', 'GET'])
def resample_audio_file_image():
    """Process the uploaded file and returns the file, and an image if requested, from disk on the server.
    """
    new_file, image = process_request()
    logging.debug('resample_audio_file_image(): Resampling audio and file and image via directory: image {} / file {}'
                  .format(image, new_file))
    return new_file, image


@app.route('/resampler/audio/url', methods=['POST', 'GET'])
def resample_audio_url():
    """Process the uploaded file and return an url to download the resampled file on the server.
    """
    new_file, image = process_request()
    server_url = 'http://localhost:5000/{}/{}'.format(app.config['RESAMPLE_FOLDER'], new_file)
    logging.debug('resample_audio_url(): Resampling audio an url to the file: {}'.format(server_url))
    return server_url


@app.route('/resampler/audio/results', methods=['GET', 'POST'])
def resample_audio_result():
    """Process the uploaded file and returns the results via a web interface
    where the plot, if requested, is shown and a way to the download the file.
    """
    new_file, image = resample_audio_file_image()
    new_file_path = os.path.join(app.config['RESAMPLE_FOLDER'], new_file)
    if image == '':
        image = '/templates/images/party.png'
    logging.debug('Resampling audio and rendering the result web-page: image {}/ file {}'.format(image, new_file_path))
    return render_template('result.html', image=image, file=new_file_path)


@app.route('/templates/images/<path:image_name>')
def load_image(image_name):
    """Send an image from a directory on the server
    """
    logging.debug('Return the image from the directory: {}/{}/{}'.format(current_app.root_path,
                                                                         app.config['IMAGE_FOLDER'], image_name))
    return send_from_directory(app.config['IMAGE_FOLDER'], current_app.root_path, image_name)


@app.route('/' + app.config['RESAMPLE_FOLDER'] + '/<path:file_name>')
def load_file(file_name):
    """Send a file from a directory on the server
    """
    logging.debug('Returning the file: {}/{}/{}'.format(current_app.root_path, app.config['RESAMPLE_FOLDER'], file_name)
                  )
    try:
        return send_from_directory(app.config['RESAMPLE_FOLDER'], current_app.root_path, file_name, as_attachment=True)
    except FileNotFoundError:
        return handle_bad_request(FileNotFoundError)


@app.route('/file-error')
def redirect():
    """Handles error related to the uploaded file
    """
    return 'File missing, or file is of wrong format, try again'


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    """Handles the exceptions
    """
    abort(Response('An Error Occurred: {}'.format(e.args[0]), 500))


if __name__ == '__main__':
    app.run(debug=False)
