import os
import time
import uuid
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory, current_app
import werkzeug
from werkzeug.utils import secure_filename

from resample import process_audio_file

# Set up the app and configure it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESAMPLE_FOLDER'] = 'resamples'
app.config['IMAGE_FOLDER'] = 'templates/images'

# Variables needed
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
SAMPLE_FREQUENCY = '32000'
ALLOWED_FREQUENCIES = [16000, 22050, 32000, 44100, 48000]


def allowed_file(filename):
    """Initial check if file is valid depending on the file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello!!'


def process_request():
    """Read parameters from the POST request
    """

    file = request.files['file']
    filename = os.path.join(app.config['RESAMPLE_FOLDER'], secure_filename(str(uuid.uuid4())))
    file.save(filename)

    if file.filename == '' or not (file and allowed_file(file.filename)):
        return redirect()

    resample_frequency = request.form.get('resample_rate')
    if resample_frequency is None:
        resample_frequency = SAMPLE_FREQUENCY

    do_plot = request.form.get('make_plot')
    if not do_plot:
        do_plot = 'False'

    new_file, image = process_audio_file(filename, int(resample_frequency), do_plot, app.config['RESAMPLE_FOLDER'])

    return new_file, image


@app.route('/resampler/audio/', methods=['POST'])
def resample_audio():
    """Loads a web-form to upload a file and allows the client to specify the sample rate and if a plot visualising
    the results are wished for
    Default value of 32000 Hz for the samples rate is used if the form is left blank
    """
    new_file, image = process_request()
    file = open(new_file, "rb")
    return file.read()


@app.route('/resampler/audio/file', methods=['POST', 'GET'])
def resample_audio_file():
    """Loads a web-form to upload a file and allows the client to specify the sample rate and if a plot visualising
    the results are wished for
    Default value of 32000 Hz for the samples rate is used if the form is left blank
    """
    new_file, image = process_request()

    return load_file(new_file)


@app.route('/resampler/audio/url', methods=['POST', 'GET'])
def resample_audio_url():
    """Loads a web-form to upload a file and allows the client to specify the sample rate and if a plot visualising
    the results are wished for
    Default value of 32000 Hz for the samples rate is used if the form is left blank
    """
    new_file, image = process_request()
    server_url = 'http://localhost:5000/{}/{}'.format(app.config['RESAMPLE_FOLDER'], new_file)
    return server_url


@app.route('/resampler/audio/results', methods=['GET', 'POST'])
def resample_audio_result():
    """ returns the results via a web interface
    where the plot, if requested, is shown and a path to the download the file is possible
    """
    new_file, image = resample_audio_file()
    new_file_path = os.path.join(app.config['RESAMPLE_FOLDER'], new_file)
    return render_template('result.html', image=image, file=new_file_path)


@app.route('/templates/images/<path:image_name>')
def load_image(image_name):
    print('im called for load_image {}'.format(image_name))
    return send_from_directory(app.config['IMAGE_FOLDER'], current_app.root_path, image_name)


@app.route('/' + app.config['RESAMPLE_FOLDER'] + '/<path:file_name>')
def load_file(file_name):
    print('im called for load_file {}'.format(file_name))
    try:
        return send_from_directory(app.config['RESAMPLE_FOLDER'], current_app.root_path, file_name, as_attachment=True)
    except FileNotFoundError:
        return handle_bad_request(FileNotFoundError)


@app.route('/file-error')
def redirect():
    return 'File missing, or file is of wrong format, try again'


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print('Exception: {}'.format(str(e)))
    print('args: {}'.format(e.args))
    return 'An Error Occurred: {}'.format(e.args[0])


if __name__ == '__main__':
    app.run(debug=True)
