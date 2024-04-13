#!/bin/bash
source_location=""

python3 -m venv venv 2>/dev/null

if [[ "$OSTYPE" == "win32" ]]; then
    source_location="venv/Scripts/activate"
else
    source_location="venv/bin/activate"
fi

source "$source_location"
python -m pip install -r requirements.txt
echo "Starting server 🔥"
flask run
