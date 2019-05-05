import hashlib
import io

def get_name(uuid):
    m = hashlib.sha1()
    m.update(uuid)
    n = int(m.hexdigest(), 16)

    lines = []
    with open("names.txt", "r") as f:
        lines = f.readlines()

    return lines[n % len(lines)].strip().lower()

def get_thing(secret):
    """Get dweet thing name from secret.
    """

    m = hashlib.sha1()
    m.update(secret)

    return m.hexdigest()

pi_cached = None

def is_raspberry_pi(raise_on_errors=False):
    """Checks if Raspberry PI.
    Thanks https://raspberrypi.stackexchange.com/a/74541
    """

    global pi_cached

    if pi_cached != None:
        return pi_cached

    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value not in (
                        'BCM2708',
                        'BCM2709',
                        'BCM2835',
                        'BCM2836'
                    ):
                        if raise_on_errors:
                            raise ValueError(
                                'This system does not appear to be a '
                                'Raspberry Pi.'
                            )
                        else:
                            pi_cached = False
                            return False
            if not found:
                if raise_on_errors:
                    raise ValueError(
                        'Unable to determine if this system is a Raspberry Pi.'
                    )
                else:
                    pi_cached = False
                    return False
    except IOError:
        if raise_on_errors:
            raise ValueError('Unable to open `/proc/cpuinfo`.')
        else:
            pi_cached = False
            return False

    pi_cached = True
    return True
