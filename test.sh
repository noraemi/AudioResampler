# File
FILE=$1
OUTPUTFILE=$2

# Install
source install.sh

# Run the flask
source run.sh

# Send a file and download the output
curl -X POST -F "file=@${FILE}" http://localhost:5000/resampler/audio/file --output ${OUTPUTFILE}

