#!/usr/bin/env bash

sudo apt update
sudo apt-get install -y python3-pip python3-venv
# sudo apt-get install python-rpi.gpio python3-rpi.gpio

# https://gpiozero.readthedocs.io/en/stable/installing.html
# sudo apt install python3-gpiozero

# create venv with py deps
python3 -m venv venv
source ./venv/bin/activate
python -m pip install requests gpiozero
