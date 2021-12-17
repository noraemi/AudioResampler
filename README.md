# Audio Sampler 
Set up a RESTful flask service to resample an audio file 
using pydub and librosa python libraries.
The file can either be processed in memory or temporary on disk.

The API support client interactions via a web-page or command line.
## Set up the environment
Run `install.sh` for bash, python installation should work for linux / mac

## Set up the server
Run `run.sh` for bash or
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
> http://localhost:5000/resampler/audio

### Test
Script provided to install, set up the server and send a file to be processed. 
The resampled file is checked to see if the conversion is successful.
> `bash test.sh` 
### API

> `resample_audio()` takes an audio file as input and returns a resampled file binaries  
> `resample_audio_file()` takes an audio file as input and returns a resampled file url on server  
> `process_request()` reads in client specified variables  
>  `file` audio file  
> `resample_frequency` desired resampling frequency  
> `do_plot` produce a validation plot
> 
> 