"""Master inteface to control and view all the Pi's
"""

from __future__ import print_function

import requests
import argparse
import dweepy

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

    for ip in ips:
        url = api_root(ip) + "/ping"

        try:
            r = requests.get(url, timeout=2)
            j = r.json()

            if 'uuid' not in j:
                gc.remove(ip)
        except:
            gc.remove(ip)

    dweepy.dweet_for(secret, {'ips': gc})

    return gc
    

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

    args = parser.parse_args()

    print("Getting all Pi's ...")

    for ip in get_addresses(args.secret):
        print(ip)
