import os
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory, current_app
import werkzeug
from werkzeug.utils import secure_filename

from resample import resample_file

# Set up the app and configure it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESAMPLE_FOLDER'] = 'resamples'
app.config['IMAGE_FOLDER'] = 'templates/images'

# Variables needed
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
SAMPLE_FREQUENCY = '32000'
ALLOWED_FREQUENCIES = [8000, 11025, 16000, 22050, 32000, 44100, 48000]


def allowed_file(filename):
    """Initial check if file is valid
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello!!'


@app.route('/upload')
def upload():
    """Landing page for uploading file via web-browser
    """
    return render_template('upload.html', srlist=ALLOWED_FREQUENCIES)


@app.route('/uploader', methods=['POST'])
def uploader():
    """Loads a web-form to upload a file and allows the client to specify the sample rate and if a plot visualising
    the results are wished for
    Default value of 32000 Hz for the samples rate is used if the form is left blank
    """
    if request.method == 'POST':
        file = request.files['file']
        resample_frequency = request.form.get('resample_rate')
        if not resample_frequency:
            resample_frequency = SAMPLE_FREQUENCY

        do_plot = request.form.get('make_plot')
        if not do_plot:
            do_plot = 'False'

        # Check whether the file exist and is either an mp3 or a wav
        if file.filename == '' or not (file and allowed_file(file.filename)):
            return redirect()
        else:
            uploaded_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(uploaded_file)
            try:
                new_file, image = resample_file(uploaded_file, app.config['RESAMPLE_FOLDER'], int(resample_frequency),
                                                do_plot)
                print('I\'m a image: {}'.format(image))
            except Exception as ex:
                return handle_bad_request(ex)

            return return_result(new_file, image)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    f = request.files['file']
    resample_frequency = request.form.get('resample_rate')
    if not resample_frequency:
        resample_frequency = SAMPLE_FREQUENCY

    if f.filename == '' or not (f and allowed_file(f.filename)):
        return redirect()
    else:
        uploaded_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(uploaded_file)
        try:
            new_file, image = resample_file(uploaded_file, int(resample_frequency), 'False')
        except Exception as ex:
            return handle_bad_request(ex)

        return 'http://localhost:5000/{}/{}'.format(app.config['RESAMPLE_FOLDER'],
                                                    Path(new_file).name)


@app.route('/return', methods=['GET'])
def return_result(file, image):
    print('Im here: {} {}'.format(file, image))
    file = Path(file).name

    filepath = os.path.join(app.config['RESAMPLE_FOLDER'] + '/' + file)

    if image == '':
        image = 'templates/images/party.png'
    return render_template('result.html', image=image, file=filepath)


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


@app.route('/wrongfile')
def redirect():
    return 'File missing, or file is of wrong format, try again'


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print('Exception: {}'.format(str(e)))
    print('args: {}'.format(e.args))
    return 'An Error Occurred: {}'.format(e.args[0])


if __name__ == '__main__':
    app.run(debug=True)
