# PiShot
![Python](https://img.shields.io/badge/python-v2.7+-blue.svg) [![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)

PiShot allows capturing high-speed strobe images using the Raspberry Pi v1
Camera. Specifically, it allows the v1 camera to operate in an open shutter mode
without a rolling shutter, and allows for precise syncing of multiple Pi's.

The project is still under active development.

![Soap](https://media.giphy.com/media/SqlCEUcH99U4Ve158v/giphy.gif)

[Bullet going through a Bar of Soap](https://media.giphy.com/media/SqlCEUcH99U4Ve158v/source.mp4)

## Setup

Enable the camera using `sudo raspi-config`. Make sure that you can take an
image using `raspistill -o test.jpeg`.

Then, install dependencies,

```
sudo apt-get install wiringpi
pip install -r requirements.txt
```

Add `dtparam=i2c_vc=on` and the end of `/boot/config.txt` and `i2c-dev` to
`/etc/modules-load.d/modules.conf`.

Then reboot.

Build the project,

```
make all
```

And then run a quick test to make sure everything is working,

```
sudo python pishot.py --one -t 10
```

This will take a 10 second exposure and save all the frames to `temp.264`.
The first time you run this, it might not work, just try it again.

**Note:** The auto white balance makes the initial images really sad. Just
wait for a minute before firing the strobe to get a better colored image.

## Usage

### Server Based

PiShot comes with a nice GUI to control each Raspberry Pi remotely, including
hostname management, remote viewing and camera alignment tools.

Configure each Pi to run the following script on boot-up,

```
python server.py --secret SECRET
```

Replace `SECRET` with a long unrecognizable string. Make sure this secret is
consistent across all PI's and make sure we write it down.

Make sure your computer / laptop is on the same network as all the Pi devices
you wish to remote control. To launch the GUI use the command,

```
python master.py --secret SECRET
```

Note that the `SECRET` here is the same secret that you used with all the Pi's.

### GPIO Based

In the event that your Raspberry Pi's don't have networking access, you can
trigger the Pi's by chaining their GPIOs.

Multiple Pi's can be daisy changed to open and close shutters at the same time.
All slave Pi's run,

```
sudo python pishot.py --slave
```

And the master Pi runs,

```
sudo python pishot.py --master
```

The Pi's must be chained as follows, (all the grounds must be tied together!)

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

This work was done by Varun Mangalick, Kristin Sheridan, Candace Okumko and
Shreyas Kapur as our final project for our class at MIT called [6.163: Strobe Project Lab](http://student.mit.edu/catalog/search.cgi?search=6.163&style=verbatim).

The work was done under the supervision of Dr. James Bales, who is an absolute
legend at helping us figure stuff out.

## License

Copyright (c) 2019 Shreyas Kapur. Released under MIT License.
