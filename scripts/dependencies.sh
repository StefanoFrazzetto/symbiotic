#!/usr/bin/env bash

sudo apt update
sudo apt-get install -y python3-dev python3-venv python3-pip
sudo apt-get install -y python3-gpiozero

## https://gpiozero.readthedocs.io/en/stable/installing.html
## sudo apt install python3-gpiozero

# start pigpio daemon
sudo pigpiod

# create venv dir
pushd ..
    python3 -m venv venv
    source ./venv/bin/activate
    python -m pip install -r requirements.txt
popd
