#!/usr/bin/env bash

# Install pigpio, so we don't have to change permissions
# for /dev/mem or /dev/gpiomem
# The daemon can be started with `sudo pigpiod`

pushd ..
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