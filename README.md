# Audio Sampler 
Set up a RESTful flask service to resample an audio file 
using the AudioSegment python library.
The file can either be processed in memory or temporary on disk.

The API support client interactions via a web-page or command line.

## Setup Environment

### Windows 10
Setup event variables and run the application
> $env:FLASK_ENV=""  
$env:FLASK_APP="application.py"  


### Linux
> FLASK_ENV=""  
> FLASK_APP="application.py"

### MAC lol who knows

## Run the server
> flask run
 
## Check if it works ...
Download a binary directly
> ```curl -X POST -F "file=@<FILE>>" http://localhost:5000/resampler/audio/file --output <OUTPUTFILE>```

or get a link to download the file
> ```curl -X POST -F "file=@<FILE>" http://localhost:5000/resampler/audio/url```

or via a web-browser interface
> http://localhost:5000/resampler/audio


### API

> `resample_audio()` takes an audio file as input and returns a resampled file binaries  
> `resample_audio_file()` takes an audio file as input and returns a resampled file url on server  
> `process_request()` reads in client specified variables  
>  `file` audio file  
> `resample_frequency` desired resampling frequency  
> `do_plot` produce a validation plot
> 
> 