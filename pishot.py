from __future__ import print_function

import os
import subprocess
import time
import signal
import cv2

import numpy as np

raspivid_process = None
trigger_process = None

def write_frex_registers():
    process = subprocess.Popen("./i2cwrite /dev/i2c-0 3002 ff".split())
    process.wait()

    process = subprocess.Popen("./i2cwrite /dev/i2c-0 3b01 00 08 00 ff ff 14 1d".split())
    process.wait()

def set_frex_trigger(on):
    val = "01" if on else "00"

    process = subprocess.Popen(("./i2cwrite /dev/i2c-0 3b08 %s" % val).split())
    process.wait()

def open_shutter():
    global raspivid_process
    global trigger_process

    if os.path.exists("temp.264"):
        os.remove("temp.264")

    raspivid_process = subprocess.Popen("raspivid -md 2 -fps 1 -pts test.pts -t 800000 -o temp.264".split())
    time.sleep(1)
    write_frex_registers()

def close_shutter(filename):
    global raspivid_process
    global trigger_process

    set_frex_trigger(False)
    if raspivid_process is None:
        return

    os.kill(raspivid_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    open_shutter()
    time.sleep(10)
    close_shutter("test.png")
