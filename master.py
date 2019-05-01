"""Master inteface to control and view all the Pi's
"""

from __future__ import print_function

import requests
import argparse
import dweepy
import webbrowser

from utils import get_name
from multiprocessing import current_process
from flask import Flask, render_template, jsonify

app = Flask(__name__)

SECRET = ""
PIS = {}

def api_root(ip):
    return "http://%s:5000" % ip

def get_addresses(secret):
    """Returns a list of all registered addresses and pings them and garbage
    collects stale addresses.
    """

    ips = []

    try:
        d = dweepy.get_latest_dweet_for(secret)
        ips = d[0]['content']['ips']
    except Exception as e:
        print(e)

    gc = ips[:]

    rv = {}

    for ip in ips:
        url = api_root(ip) + "/ping"

        try:
            r = requests.get(url, timeout=2)
            j = r.json()

            if 'uuid' not in j:
                gc.remove(ip)

            rv[j['uuid']] = ip
        except:
            gc.remove(ip)

    dweepy.dweet_for(secret, {'ips': gc})

    return rv

@app.route("/api/refresh")
def refresh_device_list():
    global SECRET
    global PIS

    PIS = get_addresses(SECRET)
    return device_list()

@app.route("/api/pis")
def device_list():
    return jsonify([{
        "uuid": uuid,
        "ip": ip,
        "name": get_name(uuid)
    } for uuid, ip in PIS.items()])

@app.route("/api/reboot/all")
def reboot_devices():
    errors = []

    for uuid, ip in PIS.items():
        try:
            requests.get(api_root(ip) + '/reboot')
        except Exception as e:
            print(e)
            errors.append(get_name(uuid))

    return jsonify({
        'errors': errors,
    })

@app.route("/api/<uuid>/reboot")
def reboot_device(uuid):
    ip = PIS.get(uuid, "")

    try:
        requests.get(api_root(ip) + '/reboot')
        return jsonify({
            'success': True,
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'error': 'error',
        })

@app.route("/")
def index():
    return render_template("app.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiShot master commander.")

    parser.add_argument(
        "--secret",
        help="A long unique string that's consistent across all Pi's",
        action="store",
        dest="secret",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--list",
        help="Just list all the available Pi's instead of running the server.",
        action="store_true",
        dest="list",
    )

    parser.add_argument(
        "--silent",
        help="Does not open a new chrome window on every restart.",
        action="store_true",
        dest="silent",
    )

    args = parser.parse_args()

    if args.list:
        print("Getting all Pi's ...")

        pis = get_addresses(args.secret)
        for ip in pis.values():
            print(ip)

        print("Found %i Pi's." % len(pis))
    else:
        SECRET = args.secret

        if not args.silent:
            webbrowser.open("http://localhost:5555")

        app.run(
            host = "0.0.0.0",
            port = 5555,
            debug = args.silent,
        )
