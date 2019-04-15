# PiShot

PiShot allows capturing high-speed strobe images using the Raspberry Pi v1
Camera. Specifically, it allows the v1 camera to operate in an open shutter mode
without a rolling shutter, and allows for precise syncing of multiple Pi's.

The project is still under active development.

## Install

Install dependencies,

```
sudo apt-get install libopencv-dev
```

Build the project,

```
make all
```

And then run it,

```
./pishot
```
