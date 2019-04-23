# PiShot

![PiShot Example](https://media.giphy.com/media/LpFQidfr2nncv47Wto/giphy.gif)

PiShot allows capturing high-speed strobe images using the Raspberry Pi v1
Camera. Specifically, it allows the v1 camera to operate in an open shutter mode
without a rolling shutter, and allows for precise syncing of multiple Pi's.

The project is still under active development.

Here is a balloon popping at two different angles:

![PiShot Example 2](https://media.giphy.com/media/H7rjlqfdurNpekRdOX/giphy.gif)

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
sudo python pishot.py --one -t 10
```

This will take a 10 second exposure and save all the frames to `temp.264`.

**Note:** The auto white balance makes the initial images really sad. Just
wait for a minute before firing the strobe to get a better colored image.

## Usage

Multiple Pi's can be daisy changed to open and close shutters at the same time.
All slave Pi's run,

```
sudo python pishot.py --slave
```

And the master Pi runs,

```
sudo python pishot.py --master
```

The Pi's must be chained as follows, (all the grounds must be tied together)

```
Master Pi's 23 --> Slave 1's 17
Slave 1's 23 --> Slave 2's 17
Slave n's 23 --> Slave (n+1)'s 17
.
.
.
```

Then, in the Master's prompt,

```
>> o
```

will open the shutter and,

```
>> c
```

will close the shutter.

## Contributors

This work was done in collaboration with Varun Mangalick, Kristin Sheridan and
Candace Okumko.

## License

Copyright (c) 2019 Shreyas Kapur. Released under MIT License.
