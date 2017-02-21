#!/bin/bash -e

if [ ! -d "venv" ]; then
    virtualenv -q venv --no-site-packages
    echo "Virtualenv created."
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Requirements installed."
