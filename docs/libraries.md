# Dependencies

## pigpio

> pigpio is a C library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO).

This library allows to control GPIO devices without the need of changing permissions for `/dev/mem` or `/dev/gpiomem`.

### Installing

```
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```

After installing the library, you can start the deamon `sudo pigpiod`.
To avoid having to start it manually, you can add a new entry to your crontab

```
$ sudo crontab -e
```

and add the following at the bottom of the file
```
@reboot      /usr/local/bin/pigpiod
```

### Notes

The default configuration might not be the most secure, so make sure to read the [documentation](http://abyz.me.uk/rpi/pigpio/) and choose the most appropriate settings for you.
