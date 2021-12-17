#!/bin/bash
# File
FILE=$1
OUTPUTFILE=$2

# Install
# source install.sh

# Run the flask
# source run.sh

# Send a file and download the output
curl -X POST -F "file=@${FILE}" http://localhost:5000/resampler/audio/file --output ${OUTPUTFILE}

# Check the sample rate of the old and new file
echo "Default file: " $FILE
python check_file.py ${FILE}

echo "Resampled file: " $OUTPUTFILE
python check_file.py ${OUTPUTFILE}

read -p 'Press enter to exit'
