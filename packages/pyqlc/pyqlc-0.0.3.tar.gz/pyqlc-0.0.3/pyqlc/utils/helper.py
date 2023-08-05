import sys

def dec_to_hex(d, n):
    return format(d, "0{}X".format(n*2))

def is_hex(h):
    try:
        int(h, 16)
        return True
    except ValueError:
        return False

def size_in_bytes(object):
    size = sys.getsizeof(object)
    return size
