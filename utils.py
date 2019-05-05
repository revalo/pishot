import hashlib

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
