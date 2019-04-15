# PiShot

PiShot allows capturing high-speed strobe images using the Raspberry Pi v1
Camera. Specifically, it allows the v1 camera to operate in an open shutter mode
without a rolling shutter, and allows for precise syncing of multiple Pi's.

The project is still under active development.

## Setup

Enable the camera using `sudo raspiconfig`. Make sure that you can take an image
using `raspistill -o test.jpeg`.

Then,

```
sudo apt-get install wiringpi
```

Add `dtparam=i2c_vc=on` and the end of `/boot/config.txt` and `i2c-dev` to
`/etc/modules-load.d/modules.conf`.

Then reboot.

Build the project,

```
make all
```

And then run it,

```
sudo python pishot.py
```
