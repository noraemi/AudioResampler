# Audio Sampler 
Set up a RESTful flask service to resample an audio file 
using pydub and librosa python libraries.
The file can either be processed in memory or temporary on disk.

The API support client interactions via a web-page or command line.
## Set up the environment
The audio sampler is based on python 3.9 version and requires ffmpeg to be installed locally

For linux
> sudo apt install ffmpeg

For win10 it works via the conda prompt
> conda install -c conda-forge ffmpeg

For mac ... this might take a while... 
> brew install ffmpeg

Run `bash install.sh` for bash, python installation should work for linux / mac.

## Set up the server
Run `bash run.sh` for bash

this might take a while for the first run, 
when you see `INFO: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` the flask is up an running

then run the `bash test.sh` while the server is up

### Windows 10
Setup event variables and run the application
> $env:FLASK_ENV=""  
$env:FLASK_APP="application.py"  

### Linux
> export FLASK_ENV=""  
> export FLASK_APP="application.py"

### MAC who knows

## Run the server
> flask run
 
## Check if it works ...
Download a binary directly
> ```curl -X POST -F "file=@<FILE>>" http://localhost:5000/resampler/audio/file --output <OUTPUTFILE>```

or get a link to download the file
> ```curl -X POST -F "file=@<FILE>" http://localhost:5000/resampler/audio/url```

or via a web-browser interface
> http://localhost:5000/resampler/

### Test
Script provided to install, set up the server and send a file to be processed. 
The resampled file is checked to see if the conversion is successful.
> `bash test.sh <input_file> <name_of_output_file>` 

file munies.mp3 available in the repo.

Requires to specify the input as argument, followed by the desired output name of the file
### API

> `resample_audio()` takes an audio file as input and returns a resampled file binaries  
> `resample_audio_file()` takes an audio file as input and returns a resampled file url on server  
> `process_request()` reads in client specified variables  
>  `file` audio file  
> `resample_frequency` desired resampling frequency  
> `do_plot` produce a validation plot
> 
> 