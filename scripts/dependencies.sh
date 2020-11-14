#!/usr/bin/env bash

sudo apt update
sudo apt-get install -y python3-dev python3-venv python3-pip
sudo apt-get install -y python3-gpiozero

# Install pigpio, so we don't have to change permissions
# for /dev/mem or /dev/gpiomem
# The daemon can be started with `sudo pigpiod`
# Read: https://gpiozero.readthedocs.io/en/stable/installing.html

SCRIPTS_DIR="$(dirname $0)"
ROOT_DIR="$SCRIPTS_DIR/.."

pushd "$ROOT_DIR"
    mkdir build
    push ./build
        wget https://github.com/joan2937/pigpio/archive/master.zip
        unzip master.zip
        cd pigpio-master
        make
        sudo make install
    popd

    rm -rf build
popd

# start pigpio daemon
sudo pigpiod

echo "### HEY, READ BEFORE YOU GO ###"
echo "Remember to add pigpiod to your crontab!"
echo "This will avoid having to manually start the daemon after reboots."
