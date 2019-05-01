"""PiShot slave server that runs on every Pi on boot.
"""

from __future__ import print_function

import socket
import dweepy
import time
import threading
import argparse

from uuid import getnode as get_mac
from flask import Flask, jsonify

app = Flask(__name__)

def get_ip():
    """Gets the IP address as a string.
    ty https://stackoverflow.com/a/1267524
    """

    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

def get_hw_id():
    return str(hex(get_mac()))

def ip_update_loop(secret, verbose):
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

        time.sleep(5)

@app.route('/ping')
def ping():
    return jsonify({"uuid": get_hw_id()})

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

    ip_thread = threading.Thread(target=ip_update_loop, args=(args.secret, args.verbose,))
    ip_thread.daemon = True
    ip_thread.start()

    app.run(host="0.0.0.0", port=5000)
