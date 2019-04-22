"""Main PiShot script.
"""

from __future__ import print_function

import os
import subprocess
import time
import signal
import argparse
import RPi.GPIO as GPIO

INPUT_PIN = 17  # Trigger pin.
CLONE_PIN = 23  # Mirror trigger pin.

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLONE_PIN, GPIO.OUT)

raspivid_process = None
trigger_process = None


def write_frex_registers():
    """Enables FREX mode on the ov5647 camera module. And sets the integration
    time to the maximum allowed.
    """

    process = subprocess.Popen("./i2cwrite /dev/i2c-0 3002 ff".split())
    process.wait()

    process = subprocess.Popen(
        "./i2cwrite /dev/i2c-0 3b01 00 08 00 ff ff 14 1d".split()
    )
    process.wait()


def open_shutter():
    """Start integrating FREX frames.
    """

    global raspivid_process
    global trigger_process

    if os.path.exists("temp.264"):
        os.remove("temp.264")

    raspivid_process = subprocess.Popen(
        "raspivid -md 2 -fps 1 --awb flash -pts test.pts -t 800000 -o temp.264".split()
    )
    time.sleep(1)
    write_frex_registers()


def close_shutter(filename):
    """Close the shutter and save the FREX frames.
    """

    global raspivid_process
    global trigger_process

    if raspivid_process is None:
        return

    os.kill(raspivid_process.pid, signal.SIGTERM)

    print("Shutter closed!")


def one_shot(t):
    """Open the shutter, wait for a bit and then close it.
    """

    open_shutter()
    time.sleep(t)
    close_shutter("test.png")


def slave_loop():
    """Operate the Pi in slave mode.
    """

    while True:
        GPIO.wait_for_edge(INPUT_PIN, GPIO.RISING)
        GPIO.output(CLONE_PIN, 1)
        open_shutter()

        GPIO.wait_for_edge(INPUT_PIN, GPIO.FALLING)
        GPIO.output(CLONE_PIN, 0)
        close_shutter("test.png")


def master_loop():
    """Operate the Pi in master mode.
    """

    while True:
        command = raw_input(">> ")

        if command == "o" or command == "open":
            GPIO.output(CLONE_PIN, 1)
            open_shutter()

        if command == "c" or command == "close":
            GPIO.output(CLONE_PIN, 0)
            close_shutter("test.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiShot main script.")

    parser.add_argument(
        "--one", default=False, action="store_true", help="Take a single shot"
    )

    parser.add_argument(
        "-t",
        help="The exposure time for --one mode.",
        action="store",
        dest="t",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--slave", default=False, action="store_true", help="Run daemon in Slave mode."
    )

    parser.add_argument(
        "--master", default=True, action="store_true", help="Run daemon in Master mode."
    )

    args = parser.parse_args()

    if args.one:
        one_shot(args.t)
    elif args.slave:
        slave_loop()
    elif args.master:
        master_loop()
