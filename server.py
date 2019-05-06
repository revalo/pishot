"""PiShot slave server that runs on every Pi on boot.
"""

from __future__ import print_function

import socket
import dweepy
import time
import threading
import argparse
import base64
import os

from utils import get_thing, is_raspberry_pi
from uuid import getnode as get_mac
from flask import Flask, jsonify, send_file

if is_raspberry_pi():
    from pishot import non_frex_shot, open_shutter, close_shutter

app = Flask(__name__)

def get_ip():
    """Gets the IP address as a string.
    ty https://stackoverflow.com/a/1267524
    """

    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

def get_hw_id():
    if not is_raspberry_pi():
        return str(hex(get_mac()))
    
    return getserial()

def ip_update_loop(secret, verbose):
    secret = get_thing(secret)

    while True:
        try:
            ips = []
            try:
                d = dweepy.get_latest_dweet_for(secret)
                ips = d[0]['content']['ips']
            except:
                pass

            ip = get_ip()
            if ip not in ips:
                ips.append(ip)
                dweepy.dweet_for(secret, {'ips': ips})

            if verbose:
                print(ips)
        except:
            pass

        time.sleep(20)

@app.route('/ping')
def ping():
    return jsonify({"uuid": get_hw_id()})

@app.route('/reboot')
def reboot():
    os.system('reboot now')
    return jsonify({"ok": "ok"})

@app.route('/capture')
def capture():
    if is_raspberry_pi():
        non_frex_shot("capture.jpg")

    with open("capture.jpg", "rb") as f:
        b64 = base64.b64encode(f.read())

    return "data:image/jpeg;base64," + b64

@app.route('/open')
def open_shutter_route():
    if is_raspberry_pi():
        open_shutter()

    return "OK"

@app.route('/close')
def close_shutter_route():
    if is_raspberry_pi():
        close_shutter()

    return "OK"

@app.route('/download')
def download_file():
    return send_file("temp.264")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiShot slave server.")

    parser.add_argument(
        "--secret",
        help="A long unique string that's consistent across all Pi's",
        action="store",
        dest="secret",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--verbose",
        help="Print out verbose messages.",
        action="store_true",
        dest="verbose",
    )

    args = parser.parse_args()

    ip_thread = threading.Thread(
        target=ip_update_loop,
        args=(args.secret, args.verbose,)
    )

    ip_thread.daemon = True
    ip_thread.start()

    app.run(host="0.0.0.0", port=5000)
