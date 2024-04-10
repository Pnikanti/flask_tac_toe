#!/bin/bash

python -m venv venv 2>/dev/null

source venv/Scripts/activate
pip install -r requirements.txt
flask run
