import hashlib

def get_name(uuid):
    m = hashlib.sha1()
    m.update(uuid)
    n = int(m.hexdigest(), 16)

    lines = []
    with open("names.txt", "r") as f:
        lines = f.readlines()

    return lines[n % len(lines)].strip().lower()
