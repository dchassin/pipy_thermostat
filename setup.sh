#!/bin/bash
if [ ! -z "$(which apt)" ]; then
    apt-get install python3-pil.imagetk
elif [ ! -z "$(which yum)" ]; then
    yum install python3-pil.imagetk
elif [ ! -z "$(which brew)" ]; then
    brew install python3-pil.imagetk
else
    echo "ERROR: cannot find installer for python3-pil.imagetk"
fi
python3 -m pip install -r requirements.txt -q -y
